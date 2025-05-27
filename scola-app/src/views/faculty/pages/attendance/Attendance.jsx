// React
import { styled } from 'nativewind';
import React, { useEffect, useState } from 'react';
import { View, Image, Text, Pressable, Modal } from 'react-native';
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

// Local Indonesia
import moment from 'moment';
import 'moment/locale/id';

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

export const AttendanceFacultyPage = ({ navigation }) => {
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
  const [dataSheet, setDataSheet] = useState([]);
  const [batchID, setBatchID] = useState(null);
  const [error, setError] = useState(null);

  // Timezone
  moment.locale('id');
  const today = moment().format('dddd');

  // Show the Modal
  const [visible, setVisible] = useState(false);

  const showModal = () => setVisible(true);
  const hideModal = () => setVisible(false);
  const containerStyle = { backgroundColor: 'white', padding: 20 };

  const backHome = () => {
    navigation.navigate('TabHomeTeacher');
  };

  const getDataSheet = async () => {
    try {
      await ApiManager.get('api/attendance_sheet', {
        method: 'GET',
      })
        .then((resp) => {
          setDataSheet(resp.data.data);
        })
        .catch((error) => {
          setError(error);
        });
    } catch {}
  };

  const setBatch = async (batchID) => {
    try {
      // as_batch_id_attend_sheet => key as async storage
      await StoreData('as_batch_id_attend_sheet', batchID);
      navigation.navigate('AttendanceSheetPage');
    } catch {}
  };

  useEffect(() => {
    getDataSheet();
  }, []);

  if (!fontsLoaded) {
    <Text>Loading...</Text>;
  } else {
    return (
      <StyledView className="bg-blue-900" style={{ flex: 1 }}>
        {/* <StyledModal
          style={{
            flex: 1,
            justifyContent: 'center',
            alignItems: 'center',
            marginTop: 22,
            backgroundColor: 'none',
          }}
          animationType="none"
          transparent={true}
          visible={visible}
          onRequestClose={() => {
            setVisible(!visible);
          }}
        >
          <View className="flex justify-center items-center h-screen bg-gray-900 opacity-90">
            <View
              className="bg-white rounded-xl shadow shadow-black p-4"
              style={{ height: '50%', width: '80%' }}
            >
              <StyledView className="flex flex-row justify-between">
                <Text
                  className="text-base"
                  style={{ fontFamily: 'Poppins_700Bold' }}
                >
                  Pilih Kelas
                </Text>
                <Pressable
                  onPress={hideModal}
                  className="bg-blue-900 p-1 rounded-xl active:bg-blue-700"
                >
                  <Image source={close} className=" h-6 w-6" />
                </Pressable>
              </StyledView>

              <StyledScrollView className="mt-3">
                {dataCourse.map((item, idx) => {
                  return (
                    <StyledView key={idx} className="mt-1">
                      <Pressable className="my-1 flex flex-row py-2 rounded-lg shadow items-center shadow-black bg-white w-90 active:bg-gray-200">
                        <Image
                          source={bookIcon}
                          className="h-6 w-6 self-center ml-2"
                        ></Image>
                        <Text className="font-bold text-blue-900 ml-3 w-3/4 text-xs">
                          {item.name}
                        </Text>
                      </Pressable>
                    </StyledView>
                  );
                })}
              </StyledScrollView>
            </View>
          </View>
        </StyledModal> */}

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
              onPress={backHome}
              className="active:border active:p-1 active:bg-gray-200 border border-transparent p-1 rounded-xl"
            >
              <StyledImage
                source={leftArrow}
                className="h-6 w-6 self-center"
              ></StyledImage>
            </Pressable>
            <StyledText
              className="text-xl ml-2 self-center"
              style={{ fontFamily: 'Poppins_700Bold' }}
            >
              Kehadiran
            </StyledText>
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
                  Pilih Kelas
                </Text>
              </StyledView>
              <StyledView className="m-6">
                <Text
                  className="text-sm"
                  style={{ fontFamily: 'Poppins_700Bold' }}
                >
                  {today}
                </Text>
              </StyledView>
            </StyledView>

            <StyledScrollView
              className="mx-3 h-96"
              persistentScrollbar={true}
              scrollIndicatorStyle={{ backgroundColor: 'pink' }}
              style={{ flex: 0.8 }}
            >
              {dataSheet.map((item, idx) => {
                return (
                  <Pressable
                    key={idx}
                    onPress={() => {
                      setBatch(item.batch_id);
                    }}
                    className="flex flex-row rounded-xl shadow shadow-gray-900 bg-white h-auto py-0.5 mx-1 my-2 active:bg-gray-200"
                    style={{ flex: 1 }}
                  >
                    <StyledView
                      className="flex flex-row ml-2"
                      style={{ flex: 0.8 }}
                    >
                      <StyledView className="flex flex-row justify-center py-3">
                        <Image
                          source={blackBoardIcon}
                          className="h-6 w-6 self-center mr-3 ml-2"
                        ></Image>
                        <StyledText
                          className="text-xs ml-2 self-center text-blue-900"
                          style={{ fontFamily: 'Poppins_700Bold' }}
                        >
                          {item.batch_name}
                        </StyledText>
                      </StyledView>
                    </StyledView>
                  </Pressable>
                );
              })}
            </StyledScrollView>
          </StyledView>
        </StyledScrollView>
      </StyledView>
    );
  }
};
