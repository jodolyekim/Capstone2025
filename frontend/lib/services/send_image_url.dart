import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:front_integration/services/firebase/firebase_auth_helper.dart';

Future<void> sendImageUrlToDjango(String imageUrl) async {
  final idToken = await getFirebaseIdToken();

  final response = await http.post(
    Uri.parse('http://10.0.2.2:8000/photos/upload/'),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer \$idToken',
    },
    body: jsonEncode({'image_url': imageUrl}),
  );

  if (response.statusCode == 200) {
    print("이미지 URL 저장 성공");
  } else {
    print("실패: \${response.body}");
  }
}