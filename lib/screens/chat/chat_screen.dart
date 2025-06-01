import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

import 'package:front_integration/services/chat_service.dart';
import 'chat_report.dart'; // 신고 화면 연결을 위해 필요

class ChatScreen extends StatefulWidget {
  final String roomId;
  final String currentUserEmail;
  final String targetUserEmail;
  final String accessToken;
  final String targetUserName; // ✅ 추가


  const ChatScreen({
    super.key,
    required this.roomId,
    required this.currentUserEmail,
    required this.targetUserEmail,
    required this.accessToken,
    required this.targetUserName, // ✅ 추가

  });

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _controller = TextEditingController();
  late ChatService chatService;
  List<Map<String, String>> messages = [];
  bool canSendMessage = true;

  
Future<void> _fetchPreviousMessages() async {
  final token = await getToken();
  if (token == null) return;

  final url = Uri.parse('http://10.0.2.2:8000/api/chat/rooms/${widget.roomId}/messages/');
  final response = await http.get(
    url,
    headers: {'Authorization': 'Bearer $token'},
  );

  if (response.statusCode == 200) {
    final List<dynamic> data = json.decode(utf8.decode(response.bodyBytes));
    setState(() {
      messages = data.map<Map<String, String>>((msg) => {
        'sender': msg['sender']?['email'] ?? '알 수 없음',
        'text': msg['input_msg'] ?? '',
        'type': msg['msg_type'] ?? 'text',
      }).toList().reversed.toList(); // 최신 메시지가 아래로
    });
  } else {
    print("❌ 메시지 불러오기 실패: ${response.statusCode}");
  }
}




@override
void initState() {
  super.initState();
  chatService = ChatService(
    chatroom: widget.roomId,
    userEmail: widget.currentUserEmail,
  );

  _checkSendPermission();

  // ✅ 과거 메시지 불러오기
  _fetchPreviousMessages();  // 🔽 아래 함수도 추가되어야 함

  // ✅ WebSocket 실시간 수신
  chatService.stream.listen((data) {
    try {
      final decoded = jsonDecode(data);
      setState(() {
        messages.add({
          'sender': decoded['sender'] ?? '알 수 없음',
          'text': decoded['filtered_msg'] ?? decoded['input_msg'] ?? decoded['message'] ?? '',
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


  Future<void> _checkSendPermission() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('accessToken');
    if (token == null) return;

    final res = await http.get(
      Uri.parse('http://10.0.2.2:8000/api/chat/can_send_message/'),
      headers: {'Authorization': 'Bearer $token'},
    );
    if (res.statusCode == 200) {
      final data = jsonDecode(res.body);
      setState(() {
        canSendMessage = data['can_send'] ?? true;
      });
    }
  }

  @override
  void dispose() {
    chatService.disconnect();
    super.dispose();
  }

  Future<void> _send() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    if (!canSendMessage) {
      _addSystemMessage("🚫 아직 메시지를 보낼 수 없습니다. 프로필을 먼저 완성해주세요.");
      return;
    }

    final token = await getToken();
    if (token == null) {
      _addSystemMessage("🚫 전송이 차단되었습니다.");
      return;
    }

    final url = Uri.parse('http://10.0.2.2:8000/api/chat/can_send_message/');
    final response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
      'message': text,
      'chatroom': widget.roomId, // ✅ 필수: 채팅방 ID 추가
      }
      ),
    );

    final resBody = jsonDecode(utf8.decode(response.bodyBytes));
    print("🔥 응답 데이터: $resBody"); // 여기에 추가

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
    Uri.parse('http://10.0.2.2:8000/api/chat/send_message_to_room/'),
  );
  request.headers['Authorization'] = 'Bearer $token';
  request.fields['chatroom'] = widget.roomId;
  request.fields['msg_type'] = 'image';
  request.fields['input_msg'] = '';
  request.files.add(await http.MultipartFile.fromPath('image', pickedFile.path));

  final response = await request.send();

  if (response.statusCode == 201) {
    final responseBody = await response.stream.bytesToString();
    final data = json.decode(responseBody);
    final imageUrl = data['filtered_msg'] ?? data['input_msg'] ?? '';

    // ✅ 상대 경로 보정
    final fullUrl = imageUrl.startsWith('http')
        ? imageUrl
        : 'http://10.0.2.2:8000$imageUrl';

    chatService.sendMessage(fullUrl, type: 'image');

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text("사진이 감지되었습니다. 보호자에게 문자가 발송되었습니다."),
        duration: Duration(seconds: 3),
      ),
    );
  } else {
    _addSystemMessage("🚫 이미지 전송 실패 (${response.statusCode})");
  }
}



  Future<void> _notifyGuardian(String imageUrl) async {
    final token = await getToken();
    if (token == null) return;

    await http.post(
      Uri.parse('http://10.0.2.2:8000/api/alerts/notify_guardian/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'message': '$imageUrl 이미지를 업로드했습니다.',
      }),
    );
  }

  Future<void> _reportMessage(String sender, String content) async {
    final token = await getToken();
    if (token == null) return;

    final response = await http.post(
      Uri.parse('http://10.0.2.2:8000/api/chat/report/'),
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'reported_user': sender,
        'message': content,
      }),
    );

    if (response.statusCode == 200) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("🚨 메시지를 신고했습니다.")),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("🚫 신고 실패")),
      );
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
  final isMe = msg['sender'] == widget.currentUserEmail;
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

  return GestureDetector(
    onLongPress: () {
      if (!isMe && msg['sender'] != 'SYSTEM') {
        showDialog(
          context: context,
          builder: (_) => AlertDialog(
            title: const Text("신고하시겠습니까?"),
            content: Text("보낸 사람: ${msg['sender']}\n메시지: ${msg['text']}"),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(context).pop();
                  _reportMessage(msg['sender']!, msg['text']!);
                },
                child: const Text("신고"),
              ),
              TextButton(
                onPressed: () => Navigator.of(context).pop(),
                child: const Text("취소"),
              ),
            ],
          ),
        );
      }
    },
    child: Align(
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
                msg['sender'] ?? '',
                style: const TextStyle(fontSize: 12, color: Colors.black54),
              ),
            const SizedBox(height: 4),
            isImage
                ? ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(
                      // ✅ 상대 경로일 경우 절대 경로로 보정
                      msg['text']!.startsWith('http')
                          ? msg['text']!
                          : 'http://10.0.2.2:8000${msg['text']!}',
                      width: 200,
                      errorBuilder: (_, __, ___) =>
                          const Text("이미지를 불러올 수 없습니다."),
                    ),
                  )
                : Text(
                    msg['text'] ?? '',
                    style: TextStyle(
                      color: isMe ? Colors.white : Colors.black87,
                      fontSize: 15,
                    ),
                  ),
          ],
        ),
      ),
    ),
  );
}


@override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(
      title: Text("${widget.targetUserName} 님과의 대화"),
      actions: [
        IconButton(
          icon: const Icon(Icons.report, color: Colors.red),
          tooltip: "신고하기",
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => ChatReportScreen(
                  roomId: widget.roomId,
                  targetUserEmail: widget.targetUserEmail,
                  accessToken: widget.accessToken,
                ),
              ),
            );
          },
        ),
      ],
    ),

    body: Column(
      children: [
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.all(10),
            itemCount: messages.length,
            itemBuilder: (_, index) =>
                _buildMessageBubble(messages[index]),
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
                  decoration: const InputDecoration.collapsed(
                      hintText: '메시지를 입력하세요'),
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