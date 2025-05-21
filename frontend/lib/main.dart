import 'package:flutter/material.dart';
import 'screens/auth/login_page.dart';
import 'screens/auth/signup_page.dart';
import 'screens/landing/landing_page.dart';
import 'screens/profile/profile_setup.dart';
import 'screens/interest/interest_page.dart';
import 'screens/interest/manual_interest_page.dart';
import 'screens/chat/chat_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Neurodiverse Dating App',
      debugShowCheckedModeBanner: false,
      initialRoute: '/',
      routes: {
        '/': (context) => const LandingPage(),
        '/login': (context) => const LoginPage(),
        '/signup': (context) => const SignupPage(),
        '/profile-setup': (context) => const ProfileSetupScreen(),
        '/interest': (context) => InterestPage(
          onFinish: () {
            Navigator.pushReplacementNamed(context, '/interest-manual');
          },
        ),
        '/interest-manual': (context) => InterestManualPage(
          onFinish: () {
            Navigator.pushReplacementNamed(context, '/');
          },
        ),
        '/chat': (context) => const ChatScreen(userEmail: 'test@example.com'),
      }
    );
  }
}
