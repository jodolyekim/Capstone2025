import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class MatchingScreen extends StatefulWidget {
  final String currentUserEmail;
  final String accessToken;

  const MatchingScreen({
    super.key,
    required this.currentUserEmail,
    required this.accessToken,
  });

  @override
  State<MatchingScreen> createState() => _MatchingScreenState();
}

class _MatchingScreenState extends State<MatchingScreen> {
  List<dynamic> candidates = [];
  int currentIndex = 0;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchCandidates();
  }

  Future<void> fetchCandidates() async {
    final url = Uri.parse('http://your.api.server/api/match/candidates/');
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer ${widget.accessToken}'},
    );

    if (response.statusCode == 200) {
      setState(() {
        candidates = jsonDecode(response.body);
        isLoading = false;
      });
    } else {
      // 오류 처리
    }
  }

  Future<void> respondToMatch(int matchId, String action) async {
    final url = Uri.parse('http://your.api.server/api/match/respond/$matchId/');
    final response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer ${widget.accessToken}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({"action": action}),
    );

    final data = jsonDecode(response.body);
    if (response.statusCode == 200 && data['chatroom_id'] != null) {
      Navigator.pushReplacementNamed(
        context,
        '/chat',
        arguments: {
          'userEmail': widget.currentUserEmail,
          'chatPartner': candidates[currentIndex]['email'],
        },
      );
    } else {
      // 다음 사용자로 이동
      setState(() {
        currentIndex++;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Scaffold(
        body: Center(child: CircularProgressIndicator()),
      );
    }

    if (currentIndex >= candidates.length) {
      return const Scaffold(
        body: Center(child: Text("추천 사용자가 더 이상 없습니다.")),
      );
    }

    final user = candidates[currentIndex];

    return Scaffold(
      appBar: AppBar(title: const Text("✨ 추천 사용자")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Card(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
          elevation: 8,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                if (user['photo'] != null)
                  Image.network(user['photo'], height: 150),
                const SizedBox(height: 12),
                Text(user['name'] ?? '이름 없음',
                    style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                Text("이메일: ${user['email']}"),
                Text("거리: ${user['distance'] ?? '알 수 없음'}"),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton.icon(
                      icon: const Icon(Icons.check),
                      label: const Text('💚 수락'),
                      onPressed: () => respondToMatch(user['match_id'], 'accept'),
                    ),
                    ElevatedButton.icon(
                      icon: const Icon(Icons.close),
                      label: const Text('❌ 거절'),
                      style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
                      onPressed: () => respondToMatch(user['match_id'], 'reject'),
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                const Text(
                  "⚠️ 먼저 거절하면 상대는 더 이상 응답할 수 없어요.",
                  style: TextStyle(color: Colors.red, fontSize: 12),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}