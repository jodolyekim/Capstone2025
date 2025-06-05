import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'manual_interest_page.dart';

class InterestPage extends StatefulWidget {
  final VoidCallback onFinish;
  const InterestPage({required this.onFinish, Key? key}) : super(key: key);

  @override
  State<InterestPage> createState() => _InterestPageState();
}

class _InterestPageState extends State<InterestPage> {
  final TextEditingController _introController = TextEditingController();
  List<String> extractedKeywords = [];
  List<String> selectedKeywords = [];
  bool isLoading = false;
  String error = '';

  Future<void> extractKeywords() async {
    final introText = _introController.text.trim();
    if (introText.length < 20) {
      setState(() {
        error = '자기소개는 최소 20자 이상 입력해주세요.';
      });
      return;
    }

    setState(() {
      isLoading = true;
      error = '';
    });

    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('accessToken');
      final email = prefs.getString('userEmail');

      if (token == null || email == null) {
        throw Exception('accessToken 또는 userEmail 없음');
      }

      // 1️⃣ 키워드 추출 요청
      final extractUrl = Uri.parse("http://10.0.2.2:8000/api/interest/gpt/");
      final extractRes = await http.post(
        extractUrl,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"intro_text": introText}),
      );

      if (extractRes.statusCode != 200) {
        throw Exception("GPT 키워드 추출 실패: ${extractRes.statusCode}");
      }

      final data = jsonDecode(utf8.decode(extractRes.bodyBytes));
      final result = data["result"];
      final flatList = <String>[];
      result.forEach((key, value) {
        if (value is List) {
          flatList.addAll(value.map((v) => v.toString()));
        }
      });

      // 2️⃣ 추출된 키워드 저장
      final saveUrl = Uri.parse("http://10.0.2.2:8000/api/interest/keywords/save/");
      final saveRes = await http.post(
        saveUrl,
        headers: {
          "Authorization": "Bearer $token",
          "Content-Type": "application/json"
        },
        body: jsonEncode(result),  // ✅ 이 부분만 고치면 끝!
      );

      if (saveRes.statusCode != 201) {
        debugPrint('⚠️ GPT 키워드 저장 실패: ${saveRes.statusCode}');
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('키워드 저장에는 실패했지만 추출은 성공했어요.')),
          );
        }
      }

      setState(() {
        extractedKeywords = flatList;
        selectedKeywords = List.from(flatList);
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        error = '에러 발생: $e';
        isLoading = false;
      });

      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(error)),
        );
      }
    }
  }

  void goToManualSelection() {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => InterestManualPage(
          onFinish: widget.onFinish,
          preselectedKeywords: selectedKeywords,
        ),
      ),
    );
  }

  Widget _buildKeywordChips() {
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: extractedKeywords.map((keyword) {
        final isSelected = selectedKeywords.contains(keyword);
        return InputChip(
          label: Text(
              keyword,
            style: TextStyle(
              fontSize: 18
            ),
          ),
          selected: isSelected,
          onSelected: (selected) {
            setState(() {
              if (selected) {
                selectedKeywords.add(keyword);
              } else {
                selectedKeywords.remove(keyword);
              }
            });
          },
          onDeleted: () {
            setState(() {
              extractedKeywords.remove(keyword);
              selectedKeywords.remove(keyword);
            });
          },
        );
      }).toList(),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('자기소개 & 키워드 추출')),
      body: Container(
        color: const Color(0xFFF9F6FC),
        padding: const EdgeInsets.all(20),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text('자기소개 (최소 20자)', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w600)),
              const SizedBox(height: 20),
              Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(12),
                  color: Colors.white,
                  boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 4)],
                ),
                child: TextField(
                  controller: _introController,
                  style: const TextStyle(fontSize: 18),
                  maxLines: 6,
                  minLines: 3,
                  decoration: const InputDecoration(
                    contentPadding: EdgeInsets.all(16),
                    border: InputBorder.none,
                    hintText: '자신의 관심사, 취향, 성격 등을 자유롭게 적어주세요.',
                  ),
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: isLoading ? null : extractKeywords,
                icon: const Icon(Icons.auto_awesome),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(vertical: 14),
                  textStyle: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
                label: isLoading
                    ? const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2),
                )
                    : const Text('GPT로 키워드 추출'),
              ),
              if (error.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.only(top: 20),
                  child: Row(
                    children: [
                      const Icon(Icons.error_outline, color: Colors.red),
                      const SizedBox(width: 8),
                      Expanded(child: Text(error, style: const TextStyle(color: Colors.red))),
                    ],
                  ),
                ),
              const SizedBox(height: 30),
              _buildKeywordChips(),
              const SizedBox(height: 30),

              if (extractedKeywords.isNotEmpty)
                Center(
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                      textStyle: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                    ),
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