import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ChatReportScreen extends StatefulWidget {
  final String roomId;
  final String targetUserEmail;
  final String accessToken;

  const ChatReportScreen({
    super.key,
    required this.roomId,
    required this.targetUserEmail,
    required this.accessToken,
  });

  @override
  State<ChatReportScreen> createState() => _ChatReportScreenState();
}

class _ChatReportScreenState extends State<ChatReportScreen> {
  String selectedReason = 'abuse';
  final TextEditingController _customReasonController = TextEditingController();

  final Map<String, String> reasonLabels = {
    'abuse': '욕설/폭언',
    'sexual': '성적 발언',
    'privacy': '개인정보 요구',
    'other': '기타',
  };

  bool isSubmitting = false;

  Future<void> _submitReport() async {
    setState(() => isSubmitting = true);

    final uri = Uri.parse('http://10.0.2.2:8000/api/chat/report/');
    final response = await http.post(
      uri,
      headers: {
        'Authorization': 'Bearer ${widget.accessToken}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'room_id': widget.roomId,
        'reason': selectedReason,
        'custom_reason':
            selectedReason == 'other' ? _customReasonController.text : '',
      }),
    );

    setState(() => isSubmitting = false);

    if (response.statusCode == 201) {
      if (mounted) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('🚨 신고가 접수되었습니다.')),
        );
      }
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('🚫 신고 실패. 다시 시도해주세요.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('채팅 신고하기')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text("신고 사유를 선택해주세요.", style: TextStyle(fontSize: 16)),
            const SizedBox(height: 16),
            ...reasonLabels.entries.map((entry) {
              return RadioListTile<String>(
                title: Text(entry.value),
                value: entry.key,
                groupValue: selectedReason,
                onChanged: (val) {
                  setState(() => selectedReason = val!);
                },
              );
            }).toList(),
            if (selectedReason == 'other') ...[
              const SizedBox(height: 10),
              const Text("기타 사유 입력"),
              TextField(
                controller: _customReasonController,
                maxLines: 3,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: '신고 사유를 입력해주세요',
                ),
              ),
            ],
            const Spacer(),
            ElevatedButton.icon(
              onPressed: isSubmitting ? null : _submitReport,
              icon: const Icon(Icons.send),
              label: const Text("신고 제출"),
              style: ElevatedButton.styleFrom(
                minimumSize: const Size.fromHeight(48),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
