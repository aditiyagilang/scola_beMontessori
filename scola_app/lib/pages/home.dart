import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:scola_app/pages/student_pages/student.dart';

class Home extends StatelessWidget {
  const Home({super.key});

  @override
  Widget build(BuildContext context) {
    return appBar(context);
  }

  Scaffold appBar(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Scola",
          style: TextStyle(
              color: Color.fromARGB(255, 26, 51, 154),
              fontSize: 18.0,
              fontFamily: String.fromEnvironment('Proxima'),
              fontWeight: FontWeight.bold),
        ),
        backgroundColor: const Color.fromARGB(255, 255, 255, 255),
        elevation: 0.0,
        centerTitle: true,
        leading: GestureDetector(
          onTap: () {},
          child: Container(
            margin: const EdgeInsets.all(10),
            alignment: Alignment.center,
            width: 37,
            decoration: BoxDecoration(
                color: const Color.fromARGB(255, 235, 235, 235), borderRadius: BorderRadius.circular(10)),
            child: SvgPicture.asset(
              'assets/icons/arrow-left.svg',
              height: 20,
              width: 20,
            ),
          ),
        ),
      ),
      body: GridView.count(
        crossAxisCount: 3,
        children: [
          Container(
            margin: const EdgeInsets.all(10.0),
            padding: const EdgeInsets.all(15.0),
            decoration: BoxDecoration(
                color: const Color.fromRGBO(255, 255, 255, 1),
                border:
                    Border.all(color: const Color.fromRGBO(255, 255, 255, 1)),
                borderRadius: const BorderRadius.all(Radius.circular(10)),
                boxShadow: const [
                  BoxShadow(
                      color: Color.fromRGBO(0, 33, 71, 0.4),
                      offset: Offset(0, 2),
                      blurRadius: 3,
                      spreadRadius: 0)
                ]),
            child: InkWell(
                onTap: () {
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => const StudentPage()));
                },
                child: Column(
                  children: [
                    Image.asset(
                      'assets/images/students.png',
                      width: 35,
                    ),
                    Container(
                      margin: const EdgeInsets.only(
                          top:
                              12.0), // Add space between the image and the text
                      child: const Text('Siswa',
                          style: TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.w500,
                              color: Color.fromRGBO(0, 33, 71, 1))),
                    ),
                  ],
                )),
          ),
        ],
      ));
  }
}
