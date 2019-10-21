package org.talosbot.utils;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ReflectUtils {

    public static List<Method> getAllMethods(Class<?> clazz) {

        List<Method> methods = new ArrayList<>();

        while (clazz != Object.class) {
            methods.addAll(Arrays.asList(clazz.getDeclaredMethods()));

            for (Class<?> inter : clazz.getInterfaces()) {
                methods.addAll(Arrays.asList(inter.getDeclaredMethods()));
            }

            clazz = clazz.getSuperclass();
        }

        return methods;
    }

    public static List<Field> getAllFields(Class<?> clazz) {

        List<Field> fields = new ArrayList<>();

        while (clazz != Object.class) {
            fields.addAll(Arrays.asList(clazz.getDeclaredFields()));

            clazz = clazz.getSuperclass();
        }

        return fields;
    }

}
