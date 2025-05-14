import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class InterestPage extends StatefulWidget {
  const InterestPage({super.key});

  @override
  State<InterestPage> createState() => _InterestPageState();
}

class _InterestPageState extends State<InterestPage> {
  final _introController = TextEditingController();
  Map<String, List<String>> extractedKeywords = {}; // 추출된 키워드 카테고리별 저장
  Set<String> removedKeywords = {}; // 삭제한 키워드
  bool isLoading = false;
  String error = '';

  Future<void> extractKeywords() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('accessToken');
    final intro = _introController.text.trim();

    if (token == null || intro.length < 20) {
      setState(() {
        error = '자기소개는 최소 20자 이상 입력해야 합니다.';
      });
      return;
    }

    setState(() {
      isLoading = true;
      error = '';
    });

    final res = await http.post(
      Uri.parse('http://10.0.2.2:8000/api/interests/extract/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: json.encode({'intro_text': intro}),
    );

    if (res.statusCode == 200) {
      final result = json.decode(res.body)['result'];
      setState(() {
        extractedKeywords = Map<String, List<String>>.from(result);
        removedKeywords.clear();
      });
    } else {
      setState(() {
        error = '키워드 추출 실패. 다시 시도해주세요.';
      });
    }

    setState(() => isLoading = false);
  }

  void removeKeyword(String category, String keyword) {
    setState(() {
      extractedKeywords[category]?.remove(keyword);
      removedKeywords.add(keyword);
      if (extractedKeywords[category]?.isEmpty ?? true) {
        extractedKeywords.remove(category);
      }
    });
  }

  Widget _buildKeywordButtons() {
    if (extractedKeywords.isEmpty) return const SizedBox();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: extractedKeywords.entries.map((entry) {
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(entry.key, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            Wrap(
              spacing: 8,
              children: entry.value.map((kw) {
                return Chip(
                  label: Text(kw),
                  deleteIcon: const Icon(Icons.close),
                  onDeleted: () => removeKeyword(entry.key, kw),
                );
              }).toList(),
            ),
            const SizedBox(height: 12),
          ],
        );
      }).toList(),
    );
  }

  void goToManualSelection() {
    Navigator.pushNamed(context, '/interest-manual', arguments: extractedKeywords);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('자기소개 & 키워드 추출')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('자기소개 (최소 20자)', style: TextStyle(fontSize: 16)),
              const SizedBox(height: 8),
              TextField(
                controller: _introController,
                maxLines: 6,
                minLines: 3,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: '자신의 관심사, 취향, 성격 등을 자유롭게 적어주세요.',
                ),
              ),
              const SizedBox(height: 16),
              ElevatedButton(
                onPressed: isLoading ? null : extractKeywords,
                child: isLoading ? const CircularProgressIndicator() : const Text('GPT로 키워드 추출'),
              ),
              if (error.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(top: 12),
                  child: Text(error, style: const TextStyle(color: Colors.red)),
                ),
              const SizedBox(height: 24),
              _buildKeywordButtons(),
              if (extractedKeywords.isNotEmpty)
                Center(
                  child: ElevatedButton(
                    onPressed: goToManualSelection,
                    child: const Text('추천 키워드 선택으로 이동'),
                  ),
                )
            ],
          ),
        ),
      ),
    );
  }
}
