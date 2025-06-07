// step4 - 보호자 기본 정보 입력 → 증명서 업로드로 이동

import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'guardian_upload.dart';

class GuardianInfoStep extends StatefulWidget {
  final VoidCallback onNext;
  final VoidCallback onBack;

  const GuardianInfoStep({super.key, required this.onNext, required this.onBack});

  @override
  State<GuardianInfoStep> createState() => _GuardianInfoStepState();
}

class _GuardianInfoStepState extends State<GuardianInfoStep> {
  final _nameController = TextEditingController();
  final _phoneController = TextEditingController();
  DateTime? _birthDate;
  String? _relation;

  Future<void> _submitGuardianInfo() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('accessToken');
    if (token == null) return;

    // 1단계: 프로필 정보에 보호자 항목 저장
    final profileUrl = Uri.parse('http://10.0.2.2:8000/api/profile/update/');
    final profileBody = {
      'protector_info_name': _nameController.text,
      'protector_info_phone': _phoneController.text,
      'protector_info_birth_date': _birthDate?.toIso8601String().split('T')[0],
      'protector_info_relationship': _relation,
    };

    final profileRes = await http.patch(
      profileUrl,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(profileBody),
    );

    if (profileRes.statusCode != 200) {
      if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('보호자 정보를 저장하는 데 실패했습니다.')),
      );
      return;
    }

    // 2단계: Guardian 객체 생성 (이미 있으면 넘어감)
    final guardianUrl = Uri.parse('http://10.0.2.2:8000/api/guardian/create/');
    final guardianBody = {
      'name': _nameController.text,
      'phone': _phoneController.text,
      'relation': _relation,
    };

    final guardianRes = await http.post(
      guardianUrl,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(guardianBody),
    );

    if (guardianRes.statusCode != 201 && guardianRes.statusCode != 400) {
      if (context.mounted) ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('보호자 모델 생성 실패')),
      );
      return;
    }

    // 3단계: 증명서 업로드 화면 이동
    widget.onNext();
  }

  void _selectBirthDate() async {
    final picked = await showDatePicker(
      context: context,
      initialDate: DateTime(1980),
      firstDate: DateTime(1900),
      lastDate: DateTime.now(),
    );
    if (picked != null) {
      setState(() {
        _birthDate = picked;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Text(
          '보호자 이름',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 10),
        TextFormField(
          controller: _nameController,
          style: const TextStyle(fontSize: 18),
          decoration: const InputDecoration(
            border: OutlineInputBorder(),
            hintText: '이름을 입력해주세요',
            contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          ),
        ),
        // TextField(
        //     controller: _nameController,
        //     style: const TextStyle(fontSize: 24),
        // ),
        const SizedBox(height: 30),
        Row(
          children: [
            const Text(
              '보호자 생년월일: ',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            Text(
              _birthDate == null ? '미지정' : _birthDate!.toLocal().toString().split(' ')[0],
              style: TextStyle(
                fontSize: 24,
                color: Colors.redAccent
              ),
            ),
          ],
        ),
        const SizedBox(height: 20),
        ElevatedButton(
          onPressed: _selectBirthDate,
          style: OutlinedButton.styleFrom(
            side: const BorderSide(color: Colors.deepPurple),
            padding: const EdgeInsets.symmetric(horizontal: 100, vertical: 14),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
          ),
          child: const Text(
              '생년월일 선택', style: TextStyle(fontSize: 18, color: Colors.deepPurple)
          ),
        ),
        const SizedBox(height: 40),
        Text(
          '보호자 전화번호',
          style: TextStyle(
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 10),
        TextFormField(
          controller: _phoneController,
          style: const TextStyle(fontSize: 18),
          decoration: const InputDecoration(
            border: OutlineInputBorder(),
            hintText: '이름을 입력해주세요',
            contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          ),
        ),

        const SizedBox(height: 30),
        const Text(
          '가족관계',
          style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold
          ),
        ),
        DropdownButtonFormField<String>(
          value: _relation,
          items: ['아빠', '엄마', '형제자매'].map((relation) {
            return DropdownMenuItem(value: relation, child: Text(relation, style: TextStyle(fontSize: 18),));
          }).toList(),
          onChanged: (val) => setState(() => _relation = val),
        ),
        const SizedBox(height: 50),



        const Spacer(),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            ElevatedButton(
                onPressed: widget.onBack,
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                  textStyle: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                child: const Text('이전')
            ),
            ElevatedButton(
                onPressed: _submitGuardianInfo,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.deepPurple[300],
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
                  textStyle: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
                child: const Text('다음')
            ),
          ],
        ),
      ],
    );
  }
}