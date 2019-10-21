package org.talosbot.utils;

import java.lang.reflect.Array;

@SuppressWarnings("unchecked")
public class ArrayUtils {

    public static <T> T[] newArray(T[] arr, int length) {
        Class<?> clazz = arr.getClass().getComponentType();
        return (T[]) Array.newInstance(clazz, length);
    }

    public static <T> T[] newArray(Class<T> clazz, int length) {
        return (T[]) Array.newInstance(clazz, length);
    }

    @SafeVarargs
    public static <T> T[] addAll(T[] arr, T... objects) {
        int len = arr.length + objects.length;
        T[] newArr = newArray(arr, len);
        for (int i = 0; i < arr.length; ++i) {
            newArr[i] = arr[i];
        }
        for (int i = arr.length; i < len; ++i) {
            newArr[i] = objects[i - arr.length];
        }
        return newArr;
    }

}
