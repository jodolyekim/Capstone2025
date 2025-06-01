import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SignupPage extends StatefulWidget {
  const SignupPage({super.key});

  @override
  State<SignupPage> createState() => _SignupPageState();
}

class _SignupPageState extends State<SignupPage> {
  final _nameController = TextEditingController(); // 현재 사용 안 함
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmController = TextEditingController();

  String error = '';
  bool signupSuccess = false;

  Future<void> signup() async {
    final email = _emailController.text.trim();
    final password = _passwordController.text;
    final confirm = _confirmController.text;

    if (password != confirm) {
      setState(() => error = "비밀번호가 일치하지 않습니다.");
      return;
    }

    final url = Uri.parse('http://10.0.2.2:8000/api/signup/');
    final res = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'email': email,
        'password': password,
        'password2': confirm,
      }),
    );

    if (res.statusCode == 200 || res.statusCode == 201) {
      final data = jsonDecode(utf8.decode(res.bodyBytes));
      final accessToken = data['access'];
      final emailFromResponse = data['email'] ?? email; // 없으면 입력값 사용

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('accessToken', accessToken);
      await prefs.setString('userEmail', emailFromResponse);

      setState(() {
        signupSuccess = true;
        error = '';
      });
    } else {
      String msg = '회원가입 실패';
      try {
        final data = jsonDecode(utf8.decode(res.bodyBytes));
        if (data is Map && data.containsKey('error')) {
          msg = '회원가입 실패: ${data['error']}';
        } else if (data is Map && data.values.isNotEmpty) {
          msg = '회원가입 실패: ${data.values.first}';
        }
      } catch (_) {
        msg = '회원가입 실패 (서버 오류)';
      }
      setState(() => error = msg);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('회원가입')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: signupSuccess
            ? Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    '회원가입이 완료되었습니다.\n지금 바로 프로필 설정을 해보시겠습니까?',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 18),
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () {
                      if (context.mounted) {
                        Navigator.pushReplacementNamed(context, '/profile-setup');
                      }
                    },
                    child: const Text('프로필 설정 바로가기'),
                  ),
                ],
              )
            : Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  TextField(
                    controller: _nameController,
                    decoration: const InputDecoration(labelText: '이름'),
                  ),
                  TextField(
                    controller: _emailController,
                    decoration: const InputDecoration(labelText: '이메일'),
                  ),
                  TextField(
                    controller: _passwordController,
                    obscureText: true,
                    decoration: const InputDecoration(labelText: '비밀번호'),
                  ),
                  TextField(
                    controller: _confirmController,
                    obscureText: true,
                    decoration: const InputDecoration(labelText: '비밀번호 확인'),
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: signup,
                    child: const Text('회원가입'),
                  ),
                  if (error.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.only(top: 12),
                      child: Text(
                        error,
                        style: const TextStyle(color: Colors.red),
                      ),
                    ),
                ],
              ),
      ),
    );
  }
}
