import pandas as pd
from sklearn import preprocessing
import numpy as np
import matplotlib.pyplot as plt


def read_csv():
    data = pd.read_csv("train.csv")
    return pd.DataFrame(data)


def show_info(df):
    print("info:")
    print(df.info)

    print("head:")
    print(df.head())

    print("tail:")
    print(df.tail())

    print("describe:")
    print(df.describe())


def encode_lable(df):
    print("!!!!!!!!!!!!!!!!!  PART 2  !!!!!!!!!!!!!!!!!")
    label_encoder = preprocessing.LabelEncoder()
    df['Sex'] = label_encoder.fit_transform(df['Sex'])
    print(df['Sex'])


def handle_nan(df):
    print("!!!!!!!!!!!!!!!!!  PART 3  !!!!!!!!!!!!!!!!!")
    print(df.isna().sum())
    # df=df.fillna(df.mean())

    df['Age'] = df['Age'].fillna(df['Age'].mean())
    df = df.drop("Cabin", axis=1)
    df['Embarked'] = df['Embarked'].fillna(0)
    # print(df['Cabin'].tail())

    print(df.isna().sum())


def delete_unnecessary_columns():
    print()


def part_5(df):
    print("!!!!!!!!!!!!!!!!!  PART 5  !!!!!!!!!!!!!!!!!")
    # print("female count:  " + str(df['Sex'].value_counts(0)))
    # print("male count:  "+ str(df['Sex'].value_counts(1)))
    # print(df["Sex"].value_counts())
    print("female count:  " + str(df[df.Sex == 0].shape[0]))
    print("male count:  " + str(df[df.Sex == 1].shape[0]))
    print("male boarded Southampton:  " +
          str(df.value_counts(["Sex", "Embarked"])[1][0]))
    # print(df.value_counts(["Sex", "Embarked"])[1][0])


def part_6(df):
    print()
    print("!!!!!!!!!!!!!!!!!  PART 6  !!!!!!!!!!!!!!!!!")
    print("passengers above 35 with ticket type 3 and with no company:  " + str(
        df.loc[(df['Age'] > 35) & (df['Pclass'] == 3) & (df['SibSp'] == 0) & (df['Parch'] == 0)].shape[0]))


def compare_vec_loop(df):
    print()
    print("!!!!!!!!!!!!!!!!!  PART 7 & 8  !!!!!!!!!!!!!!!!!")
    print("ticket price mean of Queenstown passengers(VECTORIZATION):  " +
          str(df.loc[(df['Embarked'] == 'Q')]['Fare'].mean()))
    #print(df.loc[(df['Embarked'] == 'Q')]['Fare'].mean())
    count = 0
    sum = 0
    for index, row in df.iterrows():
        if row['Embarked'] == 'Q':
            count += 1
            sum += row['Fare']
    print(sum/count)
    return


if __name__ == '__main__':
    train_df = read_csv()
    show_info(train_df)  # PART 1
    encode_lable(train_df)  # PART 2 -->  male=1  & female=0
    handle_nan(train_df)  # PART 3
    delete_unnecessary_columns()  # PART 4
    part_5(train_df)  # PART 5
    part_6(train_df)  # PART 6
    compare_vec_loop(train_df)  # PART 7 & 8
    # plt.hist(train_df)
    # plt.show()
