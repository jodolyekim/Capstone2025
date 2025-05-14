import 'package:flutter/material.dart';
import 'landing_page.dart';
import 'login_page.dart';
import 'signup_page.dart';
import 'profile_setup.dart';
import 'interest_page.dart'; // ✅ GPT 키워드 추출 화면
import 'manual_interest_page.dart'; // ✅ 수동 키워드 선택 화면
import 'package:flutter/material.dart';
import 'chat/chat_demo_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Chat Demo',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const ChatDemoScreen(),
    );
  }
}
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
        if (settings.name == '/profile-setup') {
          final args = settings.arguments as Map<String, dynamic>?;

          return MaterialPageRoute(
            builder: (context) => ProfileSetupScreen(
              initialStep: args?['initialStep'] ?? 0,
              existingData: args?['existingData'],
            ),
          );
        }
        // onGenerateRoute 내부에 추가
        if (settings.name == '/interest-manual') {
          return MaterialPageRoute(
            builder: (context) => const InterestManualPage(),
          );
        }

        switch (settings.name) {
          case '/':
            return MaterialPageRoute(builder: (_) => const LandingPage());
          case '/login':
            return MaterialPageRoute(builder: (_) => const LoginPage());
          case '/signup':
            return MaterialPageRoute(builder: (_) => const SignupPage());
          case '/interest':
            return MaterialPageRoute(builder: (_) => const InterestPage()); // ✅ GPT 화면 연결
          case '/interest-manual':
            return MaterialPageRoute(builder: (_) => const InterestManualPage()); // ✅ 수동 화면 연결
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
