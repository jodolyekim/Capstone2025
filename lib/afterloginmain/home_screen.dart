import 'package:flutter/material.dart';
import '../screens/match/match_screen.dart'; // 매칭화면
import 'chat_room_list_screen.dart'; // 채팅방 리스트
import '../screens/chat/chat_screen.dart'; // 채팅화면

class HomeScreen extends StatelessWidget {
  final String currentUserEmail;
  final String accessToken;

  const HomeScreen({
    super.key,
    required this.currentUserEmail,
    required this.accessToken,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("홈")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => MatchingScreen(
                      currentUserEmail: currentUserEmail,
                      accessToken: accessToken,
                    ),
                  ),
                );
              },
              child: const Text("매칭하기"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => ChatRoomListScreen(
                      currentUserEmail: currentUserEmail,
                      accessToken: accessToken,
                    ),
                  ),
                );
              },
              child: const Text("채팅방 들어가기"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // 🔧 테스트용 상대방 이메일
                String targetUserEmail = currentUserEmail == 'rlaworud60@naver.com'
                    ? 'rlaworud61@naver.com'
                    : 'rlaworud60@naver.com';

                // 🔧 고유 채팅방 ID 생성 (사전순 정렬)
                List<String> sorted = [currentUserEmail, targetUserEmail]..sort();
                String roomId = "${sorted[0]}_${sorted[1]}";

                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => ChatScreen(
                      roomId: roomId,
                      currentUserEmail: currentUserEmail,
                      targetUserEmail: targetUserEmail,
                      accessToken: accessToken,
                    ),
                  ),
                );
              },
              child: const Text("💬 채팅 테스트"),
            ),
          ],
        ),
      ),
    );
  }
}
