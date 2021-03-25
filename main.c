//
//  main.c
//  TP1
//
//  Created by Elliot Maisl on 23/03/2021.
//

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

void exo1_1() {
    puts("Elliot Maisl 14/07/2002\n");
}

void exo1_2() {
    puts("#####\n#\n#\n####\n#\n#\n#\n");
}

void exo1_3() {
    puts("   #####\n ##    ##\n#\n#\n#\n ##    ##\n   ####\n");
}

void exo1_4() {
    int a, b, c;
    puts("Enter 3 values:");
    scanf("%d %d %d", &a, &b, &c);
    printf("%d", (a+b+c)/3);
}

void exo1_5() {
    int len, width;
    puts("Enter length & width:");
    scanf("%d %d", &len, &width);
    printf("%d", 2 * len + 2 * width);
}

void exo1_6() {
    int days, weeks, years;
    puts("Enter number of days:");
    scanf("%d", &days);
    years = floor(days / 365);
    days %= 365;
    weeks = floor(days / 7);
    days %= 7;
    printf("%dy, %dw, %dd", years, weeks, days);
}

void exo2_1() {
    int a, b;
    puts("Enter 2 values:");
    scanf("%d %d", &a, &b);
    printf("They are %s equal", a == b ? "" : "not");
}

void exo2_2() {
    int a;
    puts("Enter a valus:");
    scanf("%d", &a);
    printf("It is %s", a % 2 ? "odd" : "even");
}

void exo2_3() {
    int a, b, c, max;
    puts("Enter 3 value:");
    scanf("%d %d %d", &a, &b, &c);
    max = a;
    if (b > max) max = b;
    if (c > max) max = c;
    printf("The biggest value is %d", max);
}

void exo2_4() {
    int a, b, c, min;
    puts("Enter 3 value:");
    scanf("%d %d %d", &a, &b, &c);
    min = a;
    if (b < min) min = b;
    if (c < min) min = c;
    printf("The smallest value is %d", min);
}

void exo2_5() {
    int year;
    puts("Enter a year:");
    scanf("%d", &year);
    if (year % 4 == 0 && (year % 100 != 0 || year % 400 == 0))
        puts("The year is leap");
    else
        puts("The year is not leap");
}

void exo2_6() {
    int a, b, c, delta;
    puts("Enter 3 coefficients");
    scanf("%d %d %d", &a, &b, &c);
    printf("Computing %dx^2 + %dx + %d\n", a, b, c);
    delta = b * b - 4 * a * c;
    if (delta < 0)
        puts("No result in ℝ");
    else if (delta == 0)
        printf("Result in ℝ: %d", -b/(2*a));
    else
        printf("Results in ℝ: %f and %f", (-b - sqrt(delta))/(2 * a), (-b + sqrt(delta))/(2 * a));
}

void exo2_7() {
    int a, b;
    char operation;
    puts("Enter a value, an operation, an int");
    scanf("%d %c %d", &a, &operation, &b);
    switch (operation) {
        case '-':
            printf("%d", a - b);
            break;
        case '+':
            printf("%d", a + b);
            break;
        case '*':
            printf("%d", a * b);
            break;
        case '/':
            printf("%d", a / b);
            break;
        default:
            puts("unknown operation");
            break;
    }
}

void exo3_1_1() {
    int a, b, i,
        total = 0;
    puts("Enter 2 values to multiply:");
    scanf("%d %d", &a, &b);
    for (i = 0; i < b; i++)
        total += a;
    printf("= %d", total);
}

void exo3_1_2() {
    int a, b, i,
        total = 0;
    puts("Enter 2 values to divide:");
    scanf("%d %d", &a, &b);
    for (i = 0; i < b; i++)
        total -= a;
    printf("= %d", total);
}

void exo3_1_3() {
    int a, b, i,
        total = 0;
    puts("Enter 2 values to power up:");
    scanf("%d %d", &a, &b);
    for (i = 0; i < b; i++)
        total *= a;
    printf("= %d", total);
}

void exo3_2() {
    int num, i,
        total = 1;
    puts("Enter a value:");
    scanf("%d", &num);
    for (i = 2; i < round(num / 2) + 1; i++) {
        if (num % i == 0)
            total += i;
    }
    printf("This number is %s perfect", total == num ? "" : "not");
}

int gcd(int a, int b) {
    if (a > b)
        return gcd(a-b, a);
    if (b > a)
        return gcd(a, b-a);
    return a;
}

void exo3_3() {
    int a, b;
    puts("Enter 2 values:");
    scanf("%d %d", &a, &b);
    printf("gcd(a, b) = %d", gcd(a, b));
}

void exo3_4() {
    int a, i, fact = 1;
    puts("Enter a values:");
    scanf("%d", &a);
    for (i = 1; i < a+1; i++)
        fact *= i;
    printf("%d! = %d", a, fact);
}

void exo3_5() {
    puts("flemme");
}

void exo3_6() {
    int num = (rand() % 1000) + 1;
    int guess = -1;
    while (guess != num) {
        puts("Make a guess:");
        scanf("%d", &guess);
        if (guess < num) {
            puts("Bigger");
        } else if (guess > num) {
            puts("Smaller");
        } else {
            puts("gg");
            return;
        }
    }
}

void exo3_7() {
    puts("flemme");
}

void exo4_1() {
    int i, size = 5;
    for (i = 0; i < size; i++)
        printf("%.*s\n", i + 1, "###########");
}

void exo4_2() {
    int i, size = 5;
    for (i = size; i >= 0; i--)
        printf("%.*s\n", i + 1, "###########");
}

void exo4_3() {
    int i, size = 5;
    for (i = 0; i < size; i++) {
        printf("%*s", size - i - 1, "");
        printf("%.*s", i * 2, "*-*-*-*-*-*-*-*-*-*-");
        printf("*\n");
    }
}

void exo4_4() {
    int i, size = 5;
    for (i = size; i >= 0; i--) {
        printf("%*s", i, "");
        printf("%.*s", (size - i) * 2, "*-*-*-*-*-*-*-*-*-*-");
        printf("*\n");
    }
}

int main() {
    exo4_4();
}
