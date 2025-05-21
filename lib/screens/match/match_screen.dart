import 'package:flutter/material.dart';

class MatchingScreen extends StatefulWidget {
  final String currentUserEmail;

  const MatchingScreen({super.key, required this.currentUserEmail});

  @override
  State<MatchingScreen> createState() => _MatchingScreenState();
}

class _MatchingScreenState extends State<MatchingScreen> {
  final Map<String, dynamic> mockUser = {
    'photoUrl': 'https://example.com/photo.jpg',
    'name': '홍길동',
    'keywords': ['산책', '책읽기', '고양이'],
    'chatStyle': '짧고 재치 있게',
    'distance': '7.4km 이내',
  };

  @override
  Widget build(BuildContext context) {
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
                Image.network(mockUser['photoUrl'] ?? '', height: 150),
                const SizedBox(height: 12),
                Text(mockUser['name'] ?? '알 수 없음',
                    style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                const SizedBox(height: 6),
                Text("관심 키워드: ${(mockUser['keywords'] as List<dynamic>).join(', ')}"),
                Text("대화 스타일: ${mockUser['chatStyle'] ?? ''}"),
                Text("거리: ${mockUser['distance'] ?? ''}"),
                const SizedBox(height: 20),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton.icon(
                      icon: const Icon(Icons.check),
                      label: const Text('💚 수락'),
                      onPressed: () async {
                        bool matched = await _handleAccept(
                          widget.currentUserEmail,
                          mockUser['name'],
                        );
                        if (matched && context.mounted) {
                          Navigator.pushReplacementNamed(
                            context,
                            '/chat',
                            arguments: {
                              'userEmail': widget.currentUserEmail,
                              'chatPartner': mockUser['name']
                            },
                          );
                        } else {
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(content: Text("상대방 수락 대기 중입니다.")),
                          );
                        }
                      },
                    ),
                    ElevatedButton.icon(
                      icon: const Icon(Icons.close),
                      label: const Text('❌ 거절'),
                      onPressed: () {
                        _handleReject(widget.currentUserEmail, mockUser['name']);
                        Navigator.pop(context);
                      },
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                const Text("⚠️ 먼저 거절하면 상대는 더 이상 응답할 수 없어요.",
                    style: TextStyle(color: Colors.red, fontSize: 12)),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Future<bool> _handleAccept(String currentUser, String otherUser) async {
    // 실제 API로 변경 예정
    await Future.delayed(const Duration(seconds: 1));
    return true; // 임시로 매칭 성공 처리
  }

  void _handleReject(String currentUser, String otherUser) {
    // 거절 API 연동 처리 예정
  }
}
