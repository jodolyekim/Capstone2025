import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _emailController = TextEditingController(); // 이메일 입력 필드 컨트롤러
  final _passwordController = TextEditingController(); // 비밀번호 입력 필드 컨트롤러

  String error = ''; // 에러 메시지 출력용
  bool showProfilePrompt = false; // 프로필 설정 유도 메시지 표시 여부
  String accessToken = ''; // 로그인 후 저장할 JWT access token
  Map<String, dynamic>? savedProfile; // 기존 프로필 정보 저장용

  // 로그인 처리 함수
  Future<void> login() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('accessToken'); // 기존 토큰 제거

    final email = _emailController.text.trim();
    final password = _passwordController.text;

    final url = Uri.parse('http://10.0.2.2:8000/api/login/');
    final res = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'email': email, 'password': password}),
    );

    if (res.statusCode == 200) {
      final responseData = json.decode(res.body);
      accessToken = responseData['access'];
      final hasProfile = responseData['is_profile_set'] ?? false;

      await prefs.setString('accessToken', accessToken); // 토큰 저장

      if (!hasProfile) {
        // 프로필 미완료인 경우, 기존 정보 불러오기
        final profileRes = await http.get(
          Uri.parse('http://10.0.2.2:8000/api/profile/'),
          headers: {'Authorization': 'Bearer $accessToken'},
        );

        if (profileRes.statusCode == 200) {
          savedProfile = json.decode(profileRes.body);
          showProfilePrompt = true;
          setState(() => error = '');
        } else {
          setState(() {
            error = '프로필 정보를 불러오지 못했습니다.';
            showProfilePrompt = false;
          });
        }
      } else {
        // 로그인 성공 시 홈으로 이동
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("로그인 성공!")),
        );
        Navigator.pushReplacementNamed(context, '/');
      }
    } else {
      // 로그인 실패 시 백엔드에서 보낸 에러 메시지 출력
      String message = '로그인 실패';
      try {
        final data = json.decode(utf8.decode(res.bodyBytes));
        if (data is Map) {
          if (data.containsKey('email')) {
            message = data['email'][0];
          } else if (data.containsKey('password')) {
            message = data['password'][0];
          } else if (data.containsKey('detail')) {
            message = data['detail'];
          }
        }
      } catch (_) {
        message = '로그인 중 오류가 발생했습니다.';
      }

      setState(() {
        error = message;
        showProfilePrompt = false;
      });
    }
  }

  // 프로필 설정 화면으로 이동
  void proceedToProfileSetup() {
    if (savedProfile == null) return;

    int nextStep = 0;

    // 현재 단계 계산
    if (savedProfile!['_name'] != null &&
        savedProfile!['_birthYMD'] != null &&
        savedProfile!['_gender'] != null &&
        savedProfile!['_sex_orientation'] != null) {
      nextStep = 1;
    }

    if (savedProfile!['_communication_way'] != null &&
        (savedProfile!['_communication_way'] as List).isNotEmpty) {
      nextStep = 2;
    }

    if (savedProfile!['_current_location_lat'] != null &&
        savedProfile!['_current_location_lon'] != null &&
        savedProfile!['_match_distance'] != null) {
      nextStep = 3;
    }

    // 프로필 설정 화면으로 이동
    Navigator.pushReplacementNamed(
      context,
      '/profile-setup',
      arguments: {
        'initialStep': nextStep,
        'existingData': savedProfile,
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('로그인')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: showProfilePrompt
            ? Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    '아직 프로필 설정이 완료되지 않았습니다.\n프로필 설정을 지금 진행하시겠습니까?',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 18),
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: proceedToProfileSetup,
                    child: const Text('프로필 설정 바로가기'),
                  )
                ],
              )
            : Column(
                children: [
                  TextField(
                    controller: _emailController,
                    decoration: const InputDecoration(labelText: '이메일'),
                  ),
                  TextField(
                    controller: _passwordController,
                    decoration: const InputDecoration(labelText: '비밀번호'),
                    obscureText: true,
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton(onPressed: login, child: const Text('로그인')),
                  if (error.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(top: 12),
                      child: Text(error, style: const TextStyle(color: Colors.red)),
                    ),
                ],
              ),
      ),
    );
  }
}
