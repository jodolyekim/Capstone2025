import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';

class ProfileSetupScreen extends StatefulWidget {
  const ProfileSetupScreen({super.key});

  @override
  State<ProfileSetupScreen> createState() => _ProfileSetupScreenState();
}

class _ProfileSetupScreenState extends State<ProfileSetupScreen> {
  int _currentStep = 0;

  final _nameController = TextEditingController();
  DateTime? _birthdate;
  String? _gender;
  String? _orientation;
  List<String> _communicationStyles = [];
  Position? _location;
  double _distance = 5;

  void _goNext() {
    if (_currentStep < 13) {
      setState(() => _currentStep++);
    }
  }

  void _goBack() {
    if (_currentStep > 0) {
      setState(() => _currentStep--);
    }
  }

  @override
  Widget build(BuildContext context) {
    List<Widget> steps = [
      Step1BasicInfo(
        nameController: _nameController,
        birthdate: _birthdate,
        gender: _gender,
        orientation: _orientation,
        onChanged: (birth, gen, ori) {
          setState(() {
            _birthdate = birth;
            _gender = gen;
            _orientation = ori;
          });
        },
      ),
      Step2Communication(
        selectedOptions: _communicationStyles,
        onChanged: (list) => setState(() => _communicationStyles = list),
      ),
      Step3Location(
        location: _location,
        onLocationRetrieved: (pos) => setState(() => _location = pos),
      ),
      Step4Distance(
        distance: _distance,
        onChanged: (val) => setState(() => _distance = val),
      ),
      for (int i = 5; i <= 14; i++) PlaceholderStep(stepNumber: i),
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text('프로필 설정 (${_currentStep + 1}/14)'),
        automaticallyImplyLeading: false,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            Expanded(child: steps[_currentStep]),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                if (_currentStep > 0)
                  ElevatedButton(onPressed: _goBack, child: const Text('이전')),
                ElevatedButton(
                  onPressed: _goNext,
                  child: Text(_currentStep == steps.length - 1 ? '완료' : '다음'),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}

// STEP 1
class Step1BasicInfo extends StatelessWidget {
  final TextEditingController nameController;
  final DateTime? birthdate;
  final String? gender;
  final String? orientation;
  final Function(DateTime?, String?, String?) onChanged;

  const Step1BasicInfo({
    super.key,
    required this.nameController,
    required this.birthdate,
    required this.gender,
    required this.orientation,
    required this.onChanged,
  });

  Future<void> _pickBirthdate(BuildContext context) async {
    final now = DateTime.now();
    final picked = await showDatePicker(
      context: context,
      initialDate: DateTime(now.year - 20),
      firstDate: DateTime(1900),
      lastDate: now,
    );
    if (picked != null) {
      onChanged(picked, gender, orientation);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        TextField(controller: nameController, decoration: const InputDecoration(labelText: '이름')),
        const SizedBox(height: 12),
        ElevatedButton(onPressed: () => _pickBirthdate(context), child: const Text('생년월일 선택')),
        if (birthdate != null) Text('선택한 날짜: ${birthdate!.toLocal().toIso8601String().split("T")[0]}'),
        const SizedBox(height: 12),
        const Text('성별 선택'),
        ...['남성', '여성', '기타'].map(
          (val) => RadioListTile(
            value: val,
            groupValue: gender,
            title: Text(val),
            onChanged: (v) => onChanged(birthdate, v, orientation),
          ),
        ),
        const Text('성적 지향'),
        ...['이성애', '동성애', '양성애', '기타'].map(
          (val) => RadioListTile(
            value: val,
            groupValue: orientation,
            title: Text(val),
            onChanged: (v) => onChanged(birthdate, gender, v),
          ),
        ),
      ],
    );
  }
}

// STEP 2
class Step2Communication extends StatelessWidget {
  final List<String> selectedOptions;
  final ValueChanged<List<String>> onChanged;

  const Step2Communication({
    super.key,
    required this.selectedOptions,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    final options = ['글로 대화하기', '천천히 말해주기', '눈 마주치지 않기', '이미지로 표현하기'];
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('커뮤니케이션 선호 방식 (복수 선택 가능)'),
        ...options.map((option) => CheckboxListTile(
              title: Text(option),
              value: selectedOptions.contains(option),
              onChanged: (val) {
                final updated = List<String>.from(selectedOptions);
                val! ? updated.add(option) : updated.remove(option);
                onChanged(updated);
              },
            )),
      ],
    );
  }
}

// STEP 3
class Step3Location extends StatelessWidget {
  final Position? location;
  final ValueChanged<Position> onLocationRetrieved;

  const Step3Location({
    super.key,
    required this.location,
    required this.onLocationRetrieved,
  });

  Future<void> _getLocation(BuildContext context) async {
    bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      await Geolocator.openLocationSettings();
      return;
    }

    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission == LocationPermission.deniedForever || permission == LocationPermission.denied) {
        return;
      }
    }

    final position = await Geolocator.getCurrentPosition();
    onLocationRetrieved(position);
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('위치 권한 및 GPS 정보 수집'),
        ElevatedButton(onPressed: () => _getLocation(context), child: const Text('내 위치 불러오기')),
        if (location != null) Text('위도: ${location!.latitude}, 경도: ${location!.longitude}'),
      ],
    );
  }
}

// STEP 4
class Step4Distance extends StatelessWidget {
  final double distance;
  final ValueChanged<double> onChanged;

  const Step4Distance({
    super.key,
    required this.distance,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('매칭 희망 거리 (km)'),
        Slider(
          value: distance,
          min: 5,
          max: 600,
          divisions: 119,
          label: '${distance.round()} km',
          onChanged: onChanged,
        ),
      ],
    );
  }
}

// STEP 5~14 껍데기용
class PlaceholderStep extends StatelessWidget {
  final int stepNumber;
  const PlaceholderStep({super.key, required this.stepNumber});

  @override
  Widget build(BuildContext context) {
    return Center(child: Text('스텝 $stepNumber 내용 (UI만 표시됨)'));
  }
}
