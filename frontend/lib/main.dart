import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

// 화면 import
import 'screens/auth/login_page.dart';
import 'screens/auth/signup_page.dart';
import 'screens/landing/landing_page.dart';
import 'screens/profile/profile_setup.dart';
import 'screens/interest/interest_page.dart';
import 'screens/interest/manual_interest_page.dart';
import 'screens/chat/chat_screen.dart';
import 'screens/match/matching_screen.dart'; // ✅ 파일명 맞췄다면 이걸로
import 'afterloginmain/home_screen.dart';
import 'afterloginmain/chat_room_list_screen.dart';

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
          onFinish: () {},
          preselectedKeywords: [],
        ),

        '/home': (context) {
          final args = ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;
          return HomeScreen(
            currentUserEmail: args['currentUserEmail'],
            accessToken: args['accessToken'],
          );
        },

        '/match': (context) {
          final args = ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;
          return FutureBuilder<bool>(
            future: checkProfileCompleted(),
            builder: (context, snapshot) {
              if (!snapshot.hasData) {
                return const Scaffold(body: Center(child: CircularProgressIndicator()));
              }
              final isSet = snapshot.data!;
              return isSet
                  ? MatchingScreen(
                currentUserEmail: args['currentUserEmail'],
                accessToken: args['accessToken'],
              )
                  : const ProfileSetupScreen();
            },
          );
        },

        '/chat-list': (context) { // ✅ 기존 chat-room-list → 통일
          final args = ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;
          return ChatRoomListScreen(
            currentUserEmail: args['currentUserEmail'],
            accessToken: args['accessToken'],
          );
        },

        '/chat-room': (context) { // ✅ 기존 chat → chat-room
          final args = ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;
          return FutureBuilder<bool>(
            future: checkProfileCompleted(),
            builder: (context, snapshot) {
              if (!snapshot.hasData) {
                return const Scaffold(body: Center(child: CircularProgressIndicator()));
              }
              final isSet = snapshot.data!;
              return isSet
                  ? ChatScreen(
                roomId: args['roomId'],
                currentUserEmail: args['currentUserEmail'],
                targetUserEmail: args['targetUserEmail'],
                targetUserName: args['targetUserName'] ?? '이름 없음',
                accessToken: args['accessToken'],
              )
                  : const ProfileSetupScreen();
            },
          );
        },
      },
    );
  }
}

Future<bool> checkProfileCompleted() async {
  final prefs = await SharedPreferences.getInstance();
  final result = prefs.getBool('isProfileSet') ?? false;
  print('🔍 isProfileSet = $result');
  return result;
}