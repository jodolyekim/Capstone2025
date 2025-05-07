import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

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

  Future<void> login() async {
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
      final token = responseData['token'];
      final hasProfile = responseData['has_profile'] ?? false;

      if (!hasProfile) {
        setState(() {
          showProfilePrompt = true;
          error = '';
        });
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("로그인 성공!")),
        );
        // TODO: 홈 화면이나 매칭 화면으로 이동
      }
    } else {
      setState(() {
        error = '로그인 실패: ${res.body}';
        showProfilePrompt = false;
      });
    }
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
                    onPressed: () {
                      Navigator.pushReplacementNamed(context, '/profile-setup');
                    },
                    child: const Text('프로필 설정 바로가기'),
                  )
                ],
              )
            : Column(
                children: [
                  TextField(controller: _emailController, decoration: const InputDecoration(labelText: '이메일')),
                  TextField(controller: _passwordController, decoration: const InputDecoration(labelText: '비밀번호'), obscureText: true),
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
