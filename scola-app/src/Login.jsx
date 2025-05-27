import React, { useState } from 'react';
import { View, Image, Text, TextInput, Pressable, Alert } from 'react-native';
import { KeyboardAvoidingScrollView } from 'react-native-keyboard-avoiding-scroll-view';
import Ionicons from '@expo/vector-icons/Ionicons';

import ApiManager from '../config/instance';
import { styled } from 'nativewind';

// Data Storage
import { StoreData } from './storage/Storage';

const StyledView = styled(View);
const StyledScrollView = styled(KeyboardAvoidingScrollView);

// Logo Scola
const logo = require('../assets/images/scola.png');

// Login Background
const bg = require('../assets/images/login-bg.png');
const studentBG = require('../assets/images/student-background.png');

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

export const Login = ({ navigation }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleLogin = async () => {
    try {
      await ApiManager.post('/web/session/authenticate', {
        method: 'POST',
        params: {
          db: 'scola',
          login: username,
          password: password,
        },
      }).then((resp) => {
        console.log('respo : ', resp.data['result']['name']);
        if (!resp.data['result']) {
          return showAlertForbidden();
        }

        if (username == '' || password == '') {
          return showAlertMandatory();
        }

        if (resp.data['result']['user_settings']) {
          StoreData('as_teacher_name', resp.data['result']['name']);
          navigation.navigate('TabHomeTeacher');
        } else {
          return showAlertForbidden();
        }
      });
    } catch (error) {
      Alert.alert(
        'Terjadi Kesalahan',
        error,
        [
          {
            text: 'Tutup',
            onPress: () => console.log('Oke pressed'),
            style: 'default', // Optional style, could be "default", "cancel", or "destructive"
          },
        ],
        { cancelable: true } // Optional, if true you can tap outside to dismiss, if false you can't
      );
    }
  };

  const handleShowPassword = async (showPassword) => {
    if (showPassword) {
      setShowPassword(false);
    } else {
      setShowPassword(true);
    }
  };

  /* Alert List */
  const showAlertForbidden = () => {
    Alert.alert(
      'Login Gagal',
      'Email atau password salah.', // Description text
      [
        {
          text: 'Tutup',
          onPress: () => console.log('Oke pressed'),
          style: 'default', // Optional style, could be "default", "cancel", or "destructive"
        },
      ],
      { cancelable: true } // Optional, if true you can tap outside to dismiss, if false you can't
    );
  };

  const showAlertMandatory = () => {
    Alert.alert(
      'Perhatian', // Title of the alert
      'Email dan password tidak boleh kosong.', // Description text
      [
        {
          text: 'Tutup', // Button text
          onPress: () => console.log('Oke pressed'), // Optional callback when button is pressed
          style: 'default', // Optional style, could be "default", "cancel", or "destructive"
        },
      ],
      { cancelable: true } // Optional, if true you can tap outside to dismiss, if false you can't
    );
  };

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
  if (!fontsLoaded) {
    <Text>Loading...</Text>;
  } else {
    return (
      <StyledScrollView className="bg-blue-900" style={{ flex: 1 }}>
        <Image
          source={bg}
          className="absolute max-w-full"
          style={{ height: '80%' }}
        ></Image>
        <Image
          source={studentBG}
          className="absolute bottom-0 max-w-full"
          style={{ height: '30%' }}
        ></Image>
        <StyledView className="h-screen mt-16" style={{ flex: 1 }}>
          <Image source={logo} className="w-screen h-28"></Image>
          <Text
            className="text-center text-2xl text-blue-900 my-7"
            style={{ fontFamily: 'Poppins_700Bold' }}
          >
            Login
          </Text>
          <StyledView className="mx-16">
            <TextInput
              className="border rounded-xl px-4 py-1"
              placeholder="Email"
              onChangeText={setUsername}
              value={username}
              autoCapitalize="none"
              keyboardType="email-address"
            />
            {showPassword ? (
              <StyledView className="w-full border rounded-xl mt-4 py-1">
                <StyledView className="flex flex-row">
                  <TextInput
                    className="flex px-4 w-full"
                    placeholder="Password"
                    onChangeText={setPassword}
                    value={password}
                    secureTextEntry={false}
                    autoCapitalize="none"
                  />
                  <Pressable
                    onPress={() => handleShowPassword(showPassword)}
                    className="ml-2 absolute right-0 mr-2"
                  >
                    <Ionicons
                      name="eye-off-outline"
                      size={24}
                      color="black"
                      className="self-center"
                    />
                  </Pressable>
                </StyledView>
              </StyledView>
            ) : (
              <StyledView className="w-full border rounded-xl mt-4 py-1">
                <StyledView className="flex flex-row">
                  <TextInput
                    className="flex px-4 w-full"
                    placeholder="Password"
                    onChangeText={setPassword}
                    value={password}
                    secureTextEntry={true}
                    autoCapitalize="none"
                  />
                  <Pressable
                    onPress={() => handleShowPassword(showPassword)}
                    className="ml-2 absolute right-0 mr-2"
                  >
                    <Ionicons
                      name="eye-outline"
                      size={24}
                      color="black"
                      className="self-center"
                    />
                  </Pressable>
                </StyledView>
              </StyledView>
            )}
          </StyledView>

          <StyledView className="mt-10 flex justify-items-center items-center">
            <Pressable
              onPress={() => handleLogin()}
              className="border border-blue-900 px-10 py-2.5 rounded-full bg-blue-900 active:bg-blue-800"
            >
              <Text
                className="text-white hover:text-black"
                style={{ fontFamily: 'Poppins_400Regular' }}
              >
                Login
              </Text>
            </Pressable>
          </StyledView>
        </StyledView>
      </StyledScrollView>
    );
  }
};
