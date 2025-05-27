// React
import { styled } from 'nativewind';
import React, { useEffect, useState } from 'react';
import {
  View,
  Image,
  Text,
  TextInput,
  Alert,
  Pressable,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  ImageBackground,
  Modal,
  Button,
} from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { RadioButton } from 'react-native-paper';
import { KeyboardAvoidingScrollView } from 'react-native-keyboard-avoiding-scroll-view';
import { FlatGrid } from 'react-native-super-grid';
import Icon from 'react-native-vector-icons/Ionicons';
import Ionicons from '@expo/vector-icons/Ionicons';

// Data Storage
import { StoreData } from '../../../../storage/Storage';
import { RetreiveData } from '../../../../storage/Storage';

// Icon
const logo = require('../../../../../assets/icons/icon.png');
const leftArrow = require('../../../../../assets/icons/left-arrow.png');
const noDataSheet = require('../../../../../assets/icons/no-data-sheet.png');
const blackBoardIcon = require('../../../../../assets/icons/blackboard.png');

// Images
const waveBG = require('../../../../../assets/images/wave.png');
const studentBG = require('../../../../../assets/images/student-background.png');

// Styled
const StyledView = styled(View);
const StyledImage = styled(Image);
const StyledText = styled(Text);
const StyledScrollView = styled(KeyboardAvoidingScrollView);
const StyledModal = styled(Modal);

// Poppins Fonts
import {
  useFonts,
  Poppins_100Thin,
  Poppins_100Thin_Italic,
  Poppins_200ExtraLight,
  Poppins_200ExtraLight_Italic,
  Poppins_300Light,
  Poppins_300Light_Italic,
  Poppins_400Regular,
  Poppins_400Regular_Italic,
  Poppins_500Medium,
  Poppins_500Medium_Italic,
  Poppins_600SemiBold,
  Poppins_600SemiBold_Italic,
  Poppins_700Bold,
  Poppins_700Bold_Italic,
  Poppins_800ExtraBold,
  Poppins_800ExtraBold_Italic,
  Poppins_900Black,
  Poppins_900Black_Italic,
} from '@expo-google-fonts/poppins';
import ApiManager from '../../../../../config/instance';
// import { AttendanceFacultyPage } from './Attendance';

export const AttendanceSheetPage = ({ navigation }) => {
  let [fontsLoaded] = useFonts({
    Poppins_100Thin,
    Poppins_100Thin_Italic,
    Poppins_200ExtraLight,
    Poppins_200ExtraLight_Italic,
    Poppins_300Light,
    Poppins_300Light_Italic,
    Poppins_400Regular,
    Poppins_400Regular_Italic,
    Poppins_500Medium,
    Poppins_500Medium_Italic,
    Poppins_600SemiBold,
    Poppins_600SemiBold_Italic,
    Poppins_700Bold,
    Poppins_700Bold_Italic,
    Poppins_800ExtraBold,
    Poppins_800ExtraBold_Italic,
    Poppins_900Black,
    Poppins_900Black_Italic,
  });

  // Data state
  const [checked, setChecked] = React.useState(false);
  const [studentBatch, setStudentBatch] = useState([]);
  const [error, setError] = useState(null);
  const today = useState();
  const [selectedValue, setSelectedValue] = useState('');
  // Show the Modal
  const [visible, setVisible] = useState(false);

  const showModal = () => setVisible(true);
  const hideModal = () => setVisible(false);
  const containerStyle = { backgroundColor: 'white', padding: 20 };

  const back = () => {
    navigation.navigate('AttendanceFacultyPage');
  };

  const getDay = async () => {};

  const postStudentBatch = async () => {
    const getBatchID = await RetreiveData('as_batch_id_attend_sheet');
    console.log('batch id : ', getBatchID);
    try {
      const postStudents = await ApiManager.post(
        `api/attendance_sheet/students/?batch_id=${getBatchID}`,
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      const attendanceStatus = postStudents.data.data.map((student) => ({
        ...student,
        present: false,
        excused: false,
        absent: false,
        late: false,
      }));
      setStudentBatch(attendanceStatus);
    } catch (error) {
      console.log('error : ', error);
    }
  };

  const changeStatusAttend = async (std_id, present, absent, excused, late) => {
    try {
      if (present === false) {
        present = true;
      } else {
        present = false;
      }
      setStudentBatch((prevStudents) =>
        prevStudents.map((student) =>
          student.id === std_id
            ? {
                ...student,
                present: present,
                absent: absent,
                excused: excused,
                late: late,
              }
            : student
        )
      );
    } catch {}
  };

  useEffect(() => {
    postStudentBatch();
    changeStatusAttend();
  }, []);

  if (!fontsLoaded) {
    <Text>Loading...</Text>;
  } else {
    return (
      <StyledView className="bg-blue-900" style={{ flex: 1 }}>
        <Image source={waveBG} className="max-w-full h-96 absolute"></Image>
        <Image
          source={studentBG}
          className="max-w-full h-60 bottom-0 flex-1 absolute"
        ></Image>

        <StyledScrollView
          horizontal={false}
          className="mt-16 mb-2 mx-4"
          style={{ flex: 1 }}
        >
          <StyledView className="flex flex-row self-start">
            <Pressable
              onPress={() => {
                back();
              }}
              className="active:border active:p-1 active:bg-gray-200 border border-transparent p-1 rounded-xl"
            >
              <StyledImage
                source={leftArrow}
                className="h-6 w-6 self-center"
              ></StyledImage>
            </Pressable>
          </StyledView>

          {/* Body */}
          <StyledView
            className="shadow shadow shadow-black bg-white mt-10 mx-1 rounded-xl mb-10"
            style={{ height: '100%', flex: 1 }}
          >
            <StyledView
              className="flex flex-row justify-between"
              style={{ flex: 0.2 }}
            >
              <StyledView className="m-6">
                <Text
                  className="text-sm"
                  style={{ fontFamily: 'Poppins_700Bold' }}
                >
                  Daftar Murid
                </Text>
              </StyledView>
            </StyledView>

            <StyledScrollView
              className="mx-3 h-96"
              persistentScrollbar={true}
              scrollIndicatorStyle={{ backgroundColor: 'pink' }}
              style={{ flex: 0.8 }}
            >
              {studentBatch.map((item, idx) => {
                return (
                  <StyledView
                    key={idx}
                    onPress={() => {
                      // setBatch(item.batch_id);
                    }}
                    className="flex flex-row justify-between border-b shadow-gray-900 bg-white h-auto py-0.5 mx-1 my-1"
                    style={{ flex: 1 }}
                  >
                    <StyledView className="self-center">
                      <StyledText
                        className="text-xs ml-2 self-center text-gray-900"
                        style={{ fontFamily: 'Poppins_700Bold' }}
                      >
                        {item.full_name}
                      </StyledText>
                    </StyledView>
                    <StyledView className="self-center flex flex-row">
                      <StyledView>
                        <RadioButton
                          color="green"
                          value="first"
                          status={item.present ? 'checked' : 'unchecked'}
                          onPress={() => {
                            changeStatusAttend(
                              item.id,
                              item.present,
                              item.absent,
                              item.excused,
                              item.late
                            );
                          }}
                        />
                      </StyledView>
                      <StyledView>
                        {/* <Picker
                          selectedValue={selectedValue}
                          onValueChange={(itemValue) =>
                            setSelectedValue(itemValue)
                          }
                        >
                          <Picker.Item label="Item 1" value="item1" />
                          <Picker.Item label="Item 2" value="item2" />
                          <Picker.Item label="Item 3" value="item3" />
                        </Picker> */}
                      </StyledView>
                    </StyledView>
                    {/* <StyledView className="flex flex-row justify-between"></StyledView> */}
                  </StyledView>
                );
              })}
            </StyledScrollView>
          </StyledView>
        </StyledScrollView>
      </StyledView>
    );
  }
};
