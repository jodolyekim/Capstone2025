import 'package:flutter/material.dart';
import 'chat_service.dart';

class ChatDemoScreen extends StatefulWidget {
  const ChatDemoScreen({super.key});

  @override
  State<ChatDemoScreen> createState() => _ChatDemoScreenState();
}

class _ChatDemoScreenState extends State<ChatDemoScreen> {
  final TextEditingController _messageController = TextEditingController();
  String _log = '';

  void _appendLog(String text) {
    setState(() => _log += '\n$text');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('📱 페이크 채팅 테스트')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(controller: _messageController, decoration: const InputDecoration(labelText: '메시지 입력')),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: () async {
                final result = await ChatService.uploadImage();
                _appendLog("📷 이미지 전송 결과: $result");
              },
              child: const Text('1️⃣ 이미지 전송 (보호자 알림)'),
            ),
            ElevatedButton(
              onPressed: () async {
                final result = await ChatService.sendMessage(_messageController.text);
                _appendLog("💬 메시지 전송 결과: $result");
              },
              child: const Text('2️⃣ 메시지 전송 (제한 조건 포함)'),
            ),
            ElevatedButton(
              onPressed: () async {
                final result = await ChatService.reportMessage();
                _appendLog("🚨 신고 결과: $result");
              },
              child: const Text('3️⃣ 메시지 신고'),
            ),
            const Divider(height: 20),
            Expanded(
              child: SingleChildScrollView(
                child: Text('📜 로그:\n$_log'),
              ),
            )
          ],
        ),
      ),
    );
  }
}
