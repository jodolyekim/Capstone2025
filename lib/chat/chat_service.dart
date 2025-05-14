import 'package:web_socket_channel/web_socket_channel.dart';
import 'dart:convert';

class ChatService {
  final String chatroom;
  final String userEmail;
  late WebSocketChannel _channel;

  ChatService({required this.chatroom, required this.userEmail}) {
    final url = Uri.parse('ws://10.0.2.2:8000/ws/chat/$chatroom/');
    try {
      _channel = WebSocketChannel.connect(url);
    } catch (e) {
      print('WebSocket connection error: $e');
      rethrow;
    }
  }

  // ✅ 외부에서 _channel 접근할 수 있도록 getter 추가
  WebSocketChannel get channel => _channel;

  // ✅ 텍스트/이미지 모두 보낼 수 있도록 메시지 타입 파라미터 추가
  void sendMessage(String inputMsg, {String type = 'text'}) {
    final message = jsonEncode({
      "sender": userEmail,
      "input_msg": inputMsg,
      "type": type,
    });
    _channel.sink.add(message);
  }

  // WebSocket 스트림
  Stream get stream => _channel.stream;

  // WebSocket 연결 종료
  void disconnect() {
    _channel.sink.close();
  }
}
