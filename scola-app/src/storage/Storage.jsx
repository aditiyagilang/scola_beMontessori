import AsyncStorage from '@react-native-async-storage/async-storage';

export const StoreData = async (key, val) => {
  try {
    const valuefy = JSON.stringify(val);
    await AsyncStorage.setItem(key, valuefy);
  } catch (err) {
    console.log(`Error : ${err}`);
  }
};

export const RetreiveData = async (key) => {
  try {
    const data = await AsyncStorage.getItem(key);
    console.log('DATA : ', data);
    if (data !== null) {
      return JSON.parse(data);
    } else {
      return `Failed to fetch the data`;
    }
  } catch (err) {
    console.log(`Error : ${err}`);
  }
};
