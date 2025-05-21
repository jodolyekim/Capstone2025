import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// 회원가입 화면
class SignupPage extends StatefulWidget {
  const SignupPage({super.key});

  @override
  State<SignupPage> createState() => _SignupPageState();
}

class _SignupPageState extends State<SignupPage> {
  // 입력 필드 컨트롤러
  final _nameController = TextEditingController(); // 현재 이름은 백엔드로 전송 X
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmController = TextEditingController();

  String error = ''; // 에러 메시지
  bool signupSuccess = false; // 회원가입 성공 여부

  // 회원가입 API 요청
  Future<void> signup() async {
    final name = _nameController.text.trim(); // 현재는 사용 X
    final email = _emailController.text.trim();
    final password = _passwordController.text;
    final confirm = _confirmController.text;

    // 비밀번호 일치 여부 확인
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

    // 회원가입 성공 시
    if (res.statusCode == 200 || res.statusCode == 201) {
      final data = jsonDecode(res.body);
      final accessToken = data['access'];

      // 토큰을 로컬에 저장
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('accessToken', accessToken);

      setState(() {
        signupSuccess = true;
        error = '';
      });
    } else {
      // 에러 메시지 파싱
      String msg = '회원가입 실패';
      try {
        final data = jsonDecode(utf8.decode(res.bodyBytes));
        if (data is Map && data.containsKey('error')) {
          msg = '회원가입 실패: ${data['error']}';
        } else if (data is Map && data.values.isNotEmpty) {
          msg = '회원가입 실패: ${data.values.first}';
        }
      } catch (e) {
        msg = '회원가입 실패 (서버 오류)';
      }
      setState(() => error = msg);
    }
  }

  // UI
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('회원가입')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: signupSuccess
        // 회원가입 완료 시
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
        // 기본 회원가입 입력 화면
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