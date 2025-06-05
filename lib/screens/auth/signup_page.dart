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
      await prefs.setString('userEmail', email); // !!! 0529 따로 추가한 부분 !!!
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
      backgroundColor: const Color(0xFFFDF7FC), // 배경색 약간 분홍빛
      appBar: AppBar(
        title: const Text('회원가입'),
        centerTitle: true,
        backgroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.only(left: 30, right: 30),
        child: Center(
          child: signupSuccess
          // 회원가입 완료 시
              ? Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.check_circle_outline,
                      color: Colors.green, size: 100),
                  const SizedBox(height: 20),
                  const Text(
                    '회원가입이 완료되었습니다!',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 12),
                  const Text(
                    '지금 바로 프로필 설정을 진행해 주세요.',
                    textAlign: TextAlign.center,
                    style: TextStyle(fontSize: 18),
                  ),
                  const SizedBox(height: 30),
                  ElevatedButton(
                      onPressed: () {
                        if (context.mounted) Navigator.pushReplacementNamed(context, '/profile-setup');
                      },
                      style: ElevatedButton.styleFrom(
                        // minimumSize: const Size(200, 50), // 버튼의 최소 크기 (가로 x 세로)
                        padding: const EdgeInsets.symmetric(horizontal: 60, vertical: 16), // 내부 여백
                        textStyle: const TextStyle( // 글자 스타일
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      child: const Text('프로필 설정 바로가기')
                  )
                ],

          )
            : Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const SizedBox(height: 30),
                const Text("환영합니다!", textAlign: TextAlign.center, style: TextStyle(fontSize: 40, fontWeight: FontWeight.w600),),
                const SizedBox(height: 30),
                buildTextField(_nameController, '이름'),
                const SizedBox(height: 30),
                buildTextField(_emailController, '이메일', keyboardType: TextInputType.emailAddress),
                const SizedBox(height: 30),
                buildTextField(_passwordController, '비밀번호', obscureText: true),
                const SizedBox(height: 30),
                buildTextField(_confirmController, '비밀번호 확인', obscureText: true),
                const SizedBox(height: 30),
                ElevatedButton(
                  onPressed: signup,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.deepPurple[300],
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(30),
                    ),
                    textStyle: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  child: const Text('회원가입'),
                ),
                if (error.isNotEmpty)
                  Padding(
                    padding: const EdgeInsets.only(top: 16),
                    child: Text(
                      error,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        color: Colors.red,
                        fontSize: 16,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
              ],
            ),
          )

        ),
    );
  }

  Widget buildTextField(TextEditingController controller, String label,
      {bool obscureText = false, TextInputType keyboardType = TextInputType.text}) {
    return TextFormField(
      controller: controller,
      obscureText: obscureText,
      keyboardType: keyboardType,
      style: const TextStyle(fontSize: 20),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 20),
        border: const OutlineInputBorder(),
        contentPadding: const EdgeInsets.symmetric(vertical: 16, horizontal: 20),
      ),
    );
  }
}