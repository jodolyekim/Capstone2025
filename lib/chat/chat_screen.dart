// ✅ 통일된 UI + 이미지 전송 예외 처리 + 시스템 메시지 개선 적용
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'package:web_socket_channel/web_socket_channel.dart';

import 'chat_service.dart';

class ChatScreen extends StatefulWidget {
  final String userEmail;

  const ChatScreen({super.key, required this.userEmail});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _controller = TextEditingController();
  late ChatService chatService;
  List<Map<String, String>> messages = [];

  @override
  void initState() {
    super.initState();
    chatService = ChatService(chatroom: 'testroom', userEmail: widget.userEmail);

    chatService.stream.listen((data) {
      try {
        final decoded = jsonDecode(data);
        setState(() {
          messages.add({
            'sender': decoded['sender'],
            'text': decoded['input_msg'],
            'type': decoded['type'] ?? 'text',
          });
        });
      } catch (e) {
        print('메시지 파싱 오류: $e');
      }
    });

    Future.delayed(Duration.zero, () {
      showDialog(
        context: context,
        builder: (_) => AlertDialog(
          title: const Text("로그인 성공"),
          content: const Text("채팅에 입장하였습니다."),
          actions: [
            TextButton(
              onPressed: () => Navigator.of(context).pop(),
              child: const Text("확인"),
            ),
          ],
        ),
      );
    });
  }

  @override
  void dispose() {
    chatService.disconnect();
    super.dispose();
  }

  Future<void> _send() async {
  final text = _controller.text.trim();
  if (text.isEmpty) return;

  final token = await getToken();
  if (token == null) {
    _addSystemMessage("🚫 전송이 차단되었습니다.");
    return;
  }

  final url = Uri.parse('http://10.0.2.2:8000/api/chat/send/');
  final response = await http.post(
    url,
    headers: {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    },
    body: jsonEncode({'message': text}),
  );

  final resBody = jsonDecode(utf8.decode(response.bodyBytes));

  if (response.statusCode != 200 || resBody['error'] != null) {
    _addSystemMessage("🚫 전송에 실패했습니다.");
    _controller.clear();
    return;
  }

  if (resBody['blocked'] == true) {
    final reasonMsg = resBody['system_message'] ?? "🚫 전송이 차단되었습니다.";
    _addSystemMessage(reasonMsg);
    _controller.clear();
    return;
  }

  chatService.sendMessage(text);
  _controller.clear();
}

  Future<void> _sendImage() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);
    if (pickedFile == null) return;

    final token = await getToken();
    if (token == null) return;

    final request = http.MultipartRequest(
      'POST',
      Uri.parse('http://10.0.2.2:8000/api/chat/upload/image/'),
    );
    request.headers['Authorization'] = 'Bearer $token';
    request.files.add(await http.MultipartFile.fromPath('image', pickedFile.path));

    final response = await request.send();
    if (response.statusCode == 200) {
      final responseBody = await response.stream.bytesToString();
      final data = json.decode(responseBody);
      final imageUrl = data['image_url'];
      chatService.sendMessage(imageUrl, type: 'image');
    } else {
      _addSystemMessage("🚫 이미지 업로드 실패 (${response.statusCode})");
    }
  }

  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('accessToken');
  }

  void _addSystemMessage(String text) {
    setState(() {
      messages.add({
        'sender': 'SYSTEM',
        'text': text,
        'type': 'text',
      });
    });
  }

  Widget _buildMessageBubble(Map<String, String> msg) {
    final isMe = msg['sender'] == widget.userEmail;
    final isImage = msg['type'] == 'image';
    final isSystem = msg['sender'] == 'SYSTEM';

    if (isSystem) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 6.0),
        child: Center(
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 6.0, horizontal: 12.0),
            decoration: BoxDecoration(
              color: Colors.grey[400],
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              msg['text'] ?? '',
              style: const TextStyle(
                color: Colors.white,
                fontSize: 13,
                fontStyle: FontStyle.italic,
              ),
            ),
          ),
        ),
      );
    }

    return Align(
      alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
        padding: const EdgeInsets.all(10),
        constraints: const BoxConstraints(maxWidth: 250),
        decoration: BoxDecoration(
          color: isMe ? Colors.blue[400] : Colors.grey[300],
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (!isMe)
              Text(
                msg['sender']!,
                style: const TextStyle(fontSize: 12, color: Colors.black54),
              ),
            const SizedBox(height: 4),
            isImage
                ? ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(
                      msg['text']!,
                      width: 200,
                      errorBuilder: (_, __, ___) => const Text("이미지를 불러올 수 없습니다."),
                    ),
                  )
                : Text(
                    msg['text']!,
                    style: TextStyle(
                      color: isMe ? Colors.white : Colors.black87,
                      fontSize: 15,
                    ),
                  ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("💬 실시간 채팅")),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(10),
              itemCount: messages.length,
              itemBuilder: (_, index) => _buildMessageBubble(messages[index]),
            ),
          ),
          const Divider(height: 1),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8),
            color: Colors.white,
            child: Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.image, color: Colors.green),
                  onPressed: _sendImage,
                ),
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration.collapsed(hintText: '메시지를 입력하세요'),
                    onSubmitted: (_) => _send(),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.send, color: Colors.blue),
                  onPressed: _send,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
