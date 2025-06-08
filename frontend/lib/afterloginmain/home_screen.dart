import 'package:flutter/material.dart';
import '../screens/match/matching_screen.dart'; // 매칭 화면
import 'chat_room_list_screen.dart'; // 채팅방 리스트 화면

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
            const SizedBox(height: 30),

            // 🟣 상단 아이콘 추가 (예: 하트 아이콘)
            const Icon(Icons.favorite, size: 80, color: Colors.deepPurple),

            const SizedBox(height: 20),

            // 🟣 환영 메시지
            const Text(
              "환영합니다!",
              style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              "마음이 통하는 사람을 만나보세요.",
              style: TextStyle(fontSize: 18, color: Colors.black54),
            ),
            const SizedBox(height: 50),
            // ✅ 매칭 화면 이동
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepPurple[400],
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 100, vertical: 20),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
                textStyle: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
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

            const SizedBox(height: 40),

            // ✅ 채팅방 목록 화면 이동
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepPurple[400],
                foregroundColor: Colors.white,
                padding: const EdgeInsets.symmetric(horizontal: 100, vertical: 20),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(30),
                ),
                textStyle: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
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

            // ✅ 채팅 테스트 버튼 제거 (실제 채팅은 채팅방 리스트에서 들어가도록)
            // ElevatedButton(
            //   onPressed: () {
            //     // 더 이상 사용하지 않음
            //   },
            //   child: const Text("💬 채팅 테스트"),
            // ),
          ],
        ),
      ),
    );
  }
}
