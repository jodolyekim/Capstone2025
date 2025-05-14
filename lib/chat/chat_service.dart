import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class ChatService {
  static const String baseUrl = "http://127.0.0.1:8000";
  static const String token = "여기에_로그인_토큰_넣기"; // Bearer 없이

  static Future<String> uploadImage() async {
    var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/api/chat/upload-image/'));
    request.headers['Authorization'] = 'Bearer $token';
    request.files.add(await http.MultipartFile.fromPath('image', 'assets/test_image.jpg')); // 더미 이미지

    try {
      var response = await request.send();
      final res = await http.Response.fromStream(response);
      return res.body;
    } catch (e) {
      return '오류: $e';
    }
  }

  static Future<String> sendMessage(String message) async {
    final res = await http.post(
      Uri.parse('$baseUrl/api/chat/send-message/'),
      headers: {
        HttpHeaders.authorizationHeader: 'Bearer $token',
        HttpHeaders.contentTypeHeader: 'application/json',
      },
      body: jsonEncode({
        "room_id": 1,
        "message": message,
        "type": "text",
      }),
    );
    return res.body;
  }

  static Future<String> reportMessage() async {
    final res = await http.post(
      Uri.parse('$baseUrl/api/chat/report-message/'),
      headers: {
        HttpHeaders.authorizationHeader: 'Bearer $token',
        HttpHeaders.contentTypeHeader: 'application/json',
      },
      body: jsonEncode({
        "message": 1,
        "reason": "비속어 사용",
      }),
    );
    return res.body;
  }
}
