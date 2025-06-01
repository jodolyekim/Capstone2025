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
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  String error = '';
  bool showProfilePrompt = false;
  String accessToken = '';
  Map<String, dynamic>? savedProfile;

  Future<void> login() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('accessToken');

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
      final stepStatus = responseData['profile_step_status'] ?? 0;
      final isApproved = responseData['is_approved'] ?? false;
      final isRejected = responseData['is_rejected'] ?? false;

      await prefs.setString('accessToken', accessToken);
      await prefs.setString('userEmail', responseData['email']);

      await Future.delayed(const Duration(milliseconds: 300));
      final checkToken = prefs.getString('accessToken');
      final checkEmail = prefs.getString('userEmail');
      print('✅ 저장 확인: $checkToken / $checkEmail');

      if (!isApproved) {
        if (context.mounted) {
          Navigator.pushNamedAndRemoveUntil(context, '/', (_) => false);
          await Future.delayed(const Duration(milliseconds: 300));
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
            content: Text(
              isRejected
                  ? '장애인등록증 혹은 가족관계증명서가 일치하지 않습니다.'
                  : '회원가입 승인을 기다려주세요.\n승인 후 로그인을 다시 시도해주세요.',
              textAlign: TextAlign.center,
            ),
            duration: const Duration(seconds: 5),
          ));
        }
        return;
      }

      final isFullyComplete = (stepStatus == 5 && isApproved);
      await prefs.setBool('isProfileSet', isFullyComplete);

      if (!isFullyComplete) {
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
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text("로그인 성공!")),
          );
          Navigator.pushReplacementNamed(
            context,
            '/home',
            arguments: {
              'currentUserEmail': responseData['email'],
              'accessToken': accessToken,
            },
          );
        }
      }
    } else {
      String message = '로그인 실패';
      try {
        final data = json.decode(utf8.decode(res.bodyBytes));
        if (data['error'] == '가입 승인이 완료되지 않았습니다.') {
          message = '회원가입 승인을 기다려주세요.\n승인 후 로그인을 다시 시도해주세요.';
        } else if (data['error'] == '가입이 거절되었습니다.') {
          message = '제출된 서류가 유효하지 않아 가입이 거절되었습니다.';
        } else {
          final keys = ['email', 'password', 'non_field_errors', 'detail', 'error'];
          for (final key in keys) {
            if (data.containsKey(key)) {
              final value = data[key];
              message = (value is List && value.isNotEmpty) ? value[0].toString() : value.toString();
              break;
            }
          }
        }
      } catch (_) {
        message = '서버 응답 해석 실패';
      }

      setState(() {
        error = message;
        showProfilePrompt = false;
      });
    }
  }

  void proceedToProfileSetup() {
    if (savedProfile == null) return;

    int nextStep = 0;
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
