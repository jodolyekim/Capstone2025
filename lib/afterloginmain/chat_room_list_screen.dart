import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import '../screens/chat/chat_screen.dart';

class ChatRoomListScreen extends StatefulWidget {
  final String currentUserEmail;
  final String accessToken;

  const ChatRoomListScreen({
    super.key,
    required this.currentUserEmail,
    required this.accessToken,
  });

  @override
  State<ChatRoomListScreen> createState() => _ChatRoomListScreenState();
}

class _ChatRoomListScreenState extends State<ChatRoomListScreen> {
  List<Map<String, dynamic>> chatRooms = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchChatRooms();
  }

  Future<void> fetchChatRooms() async {
    final url = Uri.parse('http://10.0.2.2:8000/api/chat/rooms/');
    try {
      final response = await http.get(
        url,
        headers: {
          'Authorization': 'Bearer ${widget.accessToken}',
        },
      );

      if (response.statusCode == 200) {
        final List data = json.decode(utf8.decode(response.bodyBytes));
        setState(() {
          chatRooms = data.cast<Map<String, dynamic>>();
          isLoading = false;
        });
      } else {
        debugPrint("❌ 서버 응답 오류: ${response.body}");
        setState(() => isLoading = false);
      }
    } catch (e) {
      debugPrint("❌ 네트워크 오류 또는 예외 발생: $e");
      setState(() => isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("채팅방 목록")),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : chatRooms.isEmpty
              ? const Center(child: Text("현재 참여 중인 채팅방이 없습니다."))
              : ListView.separated(
                  itemCount: chatRooms.length,
                  separatorBuilder: (_, __) => const Divider(),
                  itemBuilder: (context, index) {
                    final room = chatRooms[index];
                    return ListTile(
                      leading: const Icon(Icons.chat_bubble_outline),
                      title: Text(room['other_user_name'] ?? "상대 이름 없음"),
                      subtitle: Text("이메일: ${room['other_user_email'] ?? '알 수 없음'}"),
                      trailing: ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => ChatScreen(
                                roomId: room['chatroom'], // ✅ UUID 전달 (room_id 아님!)
                                currentUserEmail: widget.currentUserEmail,
                                targetUserEmail: room['other_user_email'],
                                targetUserName: room['other_user_name'],
                                accessToken: widget.accessToken,
                              ),
                            ),
                          );
                        },
                        child: const Text("입장"),
                      ),
                    );
                  },
                ),
    );
  }
}
