import 'package:flutter/material.dart';

class LandingPage extends StatelessWidget {
  const LandingPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white, // 배경 흰색 설정
      body: Padding(
        padding: const EdgeInsets.all(24), // 전체 패딩 설정
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center, // 세로 방향 중앙 정렬
          children: [
            const Text(
              'SPECTRUM HEARTS', // 앱 이름
              style: TextStyle(
                fontSize: 36,
                fontWeight: FontWeight.bold,
                color: Colors.pinkAccent,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 60), // 상단 여백

            // 로그인 버튼
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/login'),
              child: const Text('로그인'),
            ),
            const SizedBox(height: 16), // 버튼 사이 여백

            // 회원가입 버튼
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/signup'),
              child: const Text('회원가입'),
            ),
          ],
        ),
      ),
    );
  }
}
