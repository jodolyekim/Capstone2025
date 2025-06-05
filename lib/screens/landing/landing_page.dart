import 'package:flutter/material.dart';

class LandingPage extends StatelessWidget {
  const LandingPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFFDF7FC), // 배경 흰색 설정
      body: Padding(
        padding: const EdgeInsets.only(left: 20, right: 20), // 전체 패딩 설정
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center, // 세로 방향 중앙 정렬
          children: [
            const Text(
              'SPECTRUM HEARTS', // 앱 이름
              style: TextStyle(
                fontSize: 50,
                fontWeight: FontWeight.bold,
                color: Colors.pinkAccent,
              ),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 60), // 상단 여백

            // 로그인 버튼
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/login'),
              style: ElevatedButton.styleFrom(
                // minimumSize: const Size(200, 50), // 버튼의 최소 크기 (가로 x 세로)
                padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16), // 내부 여백
                textStyle: const TextStyle( // 글자 스타일
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              child: const Text('로그인'),
            ),
            const SizedBox(height: 30), // 버튼 사이 여백

            // 회원가입 버튼
            ElevatedButton(
              onPressed: () => Navigator.pushNamed(context, '/signup'),
              style: ElevatedButton.styleFrom(
                // minimumSize: const Size(200, 50), // 버튼의 최소 크기 (가로 x 세로)
                padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16), // 내부 여백
                textStyle: const TextStyle( // 글자 스타일
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              child: const Text('회원가입'),
            ),
          ],
        ),
      ),
    );
  }
}
