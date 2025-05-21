import 'package:http/http.dart' as http;
import 'dart:convert';
import 'firebase_auth_helper.dart';

Future<void> loginWithFirebaseToken() async {
  final idToken = await getFirebaseIdToken();

  final response = await http.post(
    Uri.parse('http://10.0.2.2:8000/api/firebase-login/'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'idToken': idToken}),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    print('로그인 성공: \${data[username]}');
  } else {
    print('로그인 실패: \${response.body}');
  }
}