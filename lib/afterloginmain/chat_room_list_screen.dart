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
    final response = await http.get(
      url,
      headers: {
        'Authorization': 'Bearer ${widget.accessToken}',
      },
    );

    print("📡 상태코드: ${response.statusCode}");
    print("📦 응답 본문: ${response.body}");

    if (response.statusCode == 200) {
      try {
        final List data = json.decode(response.body);
        print("✅ 파싱된 채팅방 수: ${data.length}");
        setState(() {
          chatRooms = data.cast<Map<String, dynamic>>();
          isLoading = false;
        });
      } catch (e) {
        print("❌ JSON 파싱 실패: $e");
        setState(() {
          isLoading = false;
        });
      }
    } else {
      debugPrint('❌ 채팅방 목록 불러오기 실패: ${response.body}');
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
              : ListView.builder(
                  itemCount: chatRooms.length,
                  itemBuilder: (context, index) {
                    final room = chatRooms[index];
                    return ListTile(
                      leading: const Icon(Icons.chat),
                      title: Text("상대방: ${room['other_user_email']}"),
                      subtitle: Text("방 ID: ${room['room_id']}"),
                      trailing: ElevatedButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => ChatScreen(
                                roomId: room['room_id'].toString(),
                                currentUserEmail: widget.currentUserEmail,
                                targetUserEmail: room['other_user_email'],
                                accessToken: widget.accessToken,
                              ),
                            ),
                          );
                        },
                        child: const Text("입장하기"),
                      ),
                    );
                  },
                ),
    );
  }
}
