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
    final url = Uri.parse('http://10.0.2.2:8000/api/match/candidates/');
    final response = await http.get(
      url,
      headers: {'Authorization': 'Bearer ${widget.accessToken}'},
    );

    if (response.statusCode == 200) {
      final decodedBody = utf8.decode(response.bodyBytes);
      final data = jsonDecode(decodedBody);

      debugPrint("✅ 후보 목록: $data");

      setState(() {
        candidates = data;
        isLoading = false;
      });
    } else {
      print('❌ 후보 목록 로딩 실패: ${response.statusCode}');
    }
  }

  Future<void> initiateMatch(int targetUserId) async {
    final url = Uri.parse('http://10.0.2.2:8000/api/match/initiate/');
    final response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer ${widget.accessToken}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({"target_user_id": targetUserId}),
    );
    print('📤 initiateMatch 요청 보냄: target_user_id = $targetUserId');
    print('📥 상태코드: ${response.statusCode}');
    print('📥 응답 본문: ${response.body}');
    try {
      final data = jsonDecode(response.body);
      final message = data['message'] ?? '처리 완료';
      final isChatCreated = data['chat_created'] == true;

      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
      }

      if (isChatCreated) {
        Navigator.pushReplacementNamed(
          context,
          '/chatList',
          arguments: {
            'currentUserEmail': widget.currentUserEmail,
            'accessToken': widget.accessToken,
          },
        );
      } else {
        setState(() {
          currentIndex++;
        });
      }
    } catch (e) {
      debugPrint('❌ initiateMatch 파싱 에러: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('❗ 서버 오류가 발생했습니다.')),
      );
    }
  }

  Future<void> respondToMatch(int targetUserId, String action) async {
    final url = Uri.parse('http://10.0.2.2:8000/api/match/respond/');
    final response = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer ${widget.accessToken}',
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        "response": action,
        "target_user_id": targetUserId,
      }),
    );

    try {
      final data = jsonDecode(response.body);
      final message = data['message'] ?? '처리 완료';
      final isChatCreated = data['chat_created'] == true;

      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
      }

      if (isChatCreated) {
        final roomId = data['room_id'];
        Navigator.pushReplacementNamed(
          context,
          '/chatRoom',
          arguments: {
            'room_id': roomId,
            'currentUserEmail': widget.currentUserEmail,
            'accessToken': widget.accessToken,
          },
        );
      } else {
        setState(() {
          currentIndex++;
        });
      }
    } catch (e) {
      debugPrint('❌ 응답 파싱 에러: $e');
      debugPrint('📦 받은 본문: ${response.body}');

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('❗ 서버 오류가 발생했습니다.')),
      );
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
      return Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text("추천 사용자가 더 이상 없습니다."),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  Navigator.pushReplacementNamed(
                    context,
                    '/home',
                    arguments: {
                      'currentUserEmail': widget.currentUserEmail,
                      'accessToken': widget.accessToken,
                    },
                  );
                },
                child: const Text("홈으로 돌아가기"),
              ),
            ],
          ),
        ),
      );
    }

    final user = candidates[currentIndex];
    final keywords = List<String>.from(user['keywords'] ?? []);
    final commonKeywords = List<String>.from(user['common_keywords'] ?? []);
    final position = user['position'] ?? "후보 ${currentIndex + 1}/${candidates.length}";

    return Scaffold(
      appBar: AppBar(title: const Text("✨ 추천 사용자"), centerTitle: true,),
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
                Text(
                  "${user['name'] ?? '이름 없음'} ($position)",
                  style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                ),
                Text("거리: ${(user['distance'] ?? '알 수 없음').toString()}"),
                const SizedBox(height: 12),
                if (keywords.isNotEmpty)
                  Wrap(
                    spacing: 6,
                    runSpacing: 4,
                    children: keywords.map<Widget>((keyword) {
                      final isCommon = commonKeywords.contains(keyword);
                      return Chip(
                        label: Text(
                          keyword,
                          style: TextStyle(
                            color: isCommon ? Colors.white : Colors.black87,
                            fontWeight: isCommon ? FontWeight.bold : FontWeight.normal,
                          ),
                        ),
                        backgroundColor: isCommon ? Colors.green : Colors.grey.shade200,
                      );
                    }).toList(),
                  ),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton.icon(
                      icon: const Icon(Icons.check),
                      label: const Text('💚 수락'),
                      onPressed: () {
                        final id = user['user_id'];
                        if (id != null && id is int) {
                          respondToMatch(id, 'accept');
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('사용자 ID가 유효하지 않습니다.')),
                          );
                        }
                      },
                    ),
                    ElevatedButton.icon(
                      icon: const Icon(Icons.close),
                      label: const Text('❌ 거절'),
                      // style: ElevatedButton.styleFrom(backgroundColor: Colors.redAccent),
                      onPressed: () {
                        final id = user['user_id'];
                        if (id != null && id is int) {
                          respondToMatch(id, 'reject');
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text('사용자 ID가 유효하지 않습니다.')),
                          );
                        }
                      },
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                const Text(
                  "⚠️ 먼저 거절하면 상대는 더 이상 응답할 수 없어요.",
                  style: TextStyle(color: Colors.red, fontSize: 15),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  } // <-- build 함수 닫기

} // <-- _MatchingScreenState 클래스 닫기