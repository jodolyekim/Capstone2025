import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class InterestManualPage extends StatefulWidget {
  const InterestManualPage({super.key});

  @override
  State<InterestManualPage> createState() => _InterestManualPageState();
}

class _InterestManualPageState extends State<InterestManualPage> {
  Map<String, List<String>> recommendedKeywords = {}; // 카테고리별 키워드
  String selectedCategory = ''; // 현재 선택된 탭
  Set<String> selectedKeywords = {}; // 사용자가 선택한 키워드
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchRecommendedKeywords();
  }

  Future<void> fetchRecommendedKeywords() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('accessToken');
    if (token == null) return;

    final url = Uri.parse('http://10.0.2.2:8000/api/interests/manual/recommend/');
    final res = await http.get(url, headers: {
      'Authorization': 'Bearer $token'
    });

    if (res.statusCode == 200) {
      final data = json.decode(utf8.decode(res.bodyBytes));
      setState(() {
        recommendedKeywords = Map<String, List<String>>.from(
          data.map((key, value) => MapEntry(key, List<String>.from(value)))
        );
        selectedCategory = recommendedKeywords.keys.first;
        isLoading = false;
      });
    } else {
      setState(() => isLoading = false);
    }
  }

  Future<void> saveSelectedKeywords() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('accessToken');
    if (token == null) return;

    final url = Uri.parse('http://10.0.2.2:8000/api/interests/manual/save/');
    final res = await http.post(
      url,
      headers: {
        'Authorization': 'Bearer $token',
        'Content-Type': 'application/json'
      },
      body: json.encode({
        'category': selectedCategory,
        'keywords': selectedKeywords.toList()
      })
    );

    if (res.statusCode == 201) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('키워드가 저장되었습니다.')),
      );
      Navigator.pushReplacementNamed(context, '/');
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('저장에 실패했습니다.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    final categoryTabs = recommendedKeywords.keys.toList();
    final keywords = recommendedKeywords[selectedCategory] ?? [];

    return Scaffold(
      appBar: AppBar(title: const Text('관심 키워드 선택')),
      body: Column(
        children: [
          SizedBox(
            height: 50,
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: categoryTabs.length,
              itemBuilder: (context, index) {
                final category = categoryTabs[index];
                final isSelected = category == selectedCategory;
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 8),
                  child: ChoiceChip(
                    label: Text(category),
                    selected: isSelected,
                    onSelected: (_) {
                      setState(() => selectedCategory = category);
                    },
                  ),
                );
              },
            ),
          ),
          const SizedBox(height: 20),
          Wrap(
            spacing: 10,
            children: keywords.map((keyword) {
              final isSelected = selectedKeywords.contains(keyword);
              return FilterChip(
                label: Text(keyword),
                selected: isSelected,
                onSelected: (bool selected) {
                  setState(() {
                    if (selected && selectedKeywords.length < 10) {
                      selectedKeywords.add(keyword);
                    } else {
                      selectedKeywords.remove(keyword);
                    }
                  });
                },
              );
            }).toList(),
          ),
          const Spacer(),
          Text('선택한 키워드: ${selectedKeywords.length} / 10'),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 16.0),
            child: ElevatedButton(
              onPressed: selectedKeywords.length >= 3 ? saveSelectedKeywords : null,
              child: const Text('선택 키워드 저장'),
            ),
          )
        ],
      ),
    );
  }
}
