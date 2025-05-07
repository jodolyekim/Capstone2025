import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SignupPage extends StatefulWidget {
  const SignupPage({super.key});

  @override
  State<SignupPage> createState() => _SignupPageState();
}

class _SignupPageState extends State<SignupPage> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmController = TextEditingController();

  String error = '';
  bool signupSuccess = false;

  Future<void> signup() async {
    final name = _nameController.text.trim();
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
        'username': name,
        'email': email,
        'password': password,
        'password2': confirm,
      }),
    );

    if (res.statusCode == 200 || res.statusCode == 201) {
      setState(() {
        signupSuccess = true;
        error = '';
      });
    } else {
      setState(() => error = '회원가입 실패: ${res.body}');
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
                      Navigator.pushReplacementNamed(context, '/profile-setup');
                    },
                    child: const Text('프로필 설정 바로가기'),
                  )
                ],
              )
            : Column(
                children: [
                  TextField(controller: _nameController, decoration: const InputDecoration(labelText: '이름')),
                  TextField(controller: _emailController, decoration: const InputDecoration(labelText: '이메일')),
                  TextField(controller: _passwordController, decoration: const InputDecoration(labelText: '비밀번호'), obscureText: true),
                  TextField(controller: _confirmController, decoration: const InputDecoration(labelText: '비밀번호 확인'), obscureText: true),
                  const SizedBox(height: 20),
                  ElevatedButton(onPressed: signup, child: const Text('회원가입')),
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
