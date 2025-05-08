import 'package:flutter/material.dart';
import 'landing_page.dart';
import 'login_page.dart';
import 'signup_page.dart';
import 'profile_setup.dart';

void main() {
  // 앱 실행 진입점
  runApp(const MyApp());
}

// 전체 앱의 루트 위젯
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Heart Spectrum',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.pink,
        fontFamily: 'Roboto',
      ),
      initialRoute: '/',
      onGenerateRoute: (settings) {
        // 프로필 설정 화면의 경우 arguments로 초기 상태와 기존 데이터를 전달받아 처리
        if (settings.name == '/profile-setup') {
          final args = settings.arguments as Map<String, dynamic>?;

          return MaterialPageRoute(
            builder: (context) => ProfileSetupScreen(
              initialStep: args?['initialStep'] ?? 0,
              existingData: args?['existingData'],
            ),
          );
        }

        // 나머지 일반적인 라우트들
        switch (settings.name) {
          case '/':
            return MaterialPageRoute(builder: (_) => const LandingPage());
          case '/login':
            return MaterialPageRoute(builder: (_) => const LoginPage());
          case '/signup':
            return MaterialPageRoute(builder: (_) => const SignupPage());
          default:
            return MaterialPageRoute(
              builder: (_) => Scaffold(
                body: Center(child: Text('존재하지 않는 경로입니다: ${settings.name}')),
              ),
            );
        }
      },
    );
  }
}
