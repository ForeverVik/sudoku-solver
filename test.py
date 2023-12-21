def main():
    l1 = [1,2,3,4,5]
    l2 = [1,4]
    res = all(ele in l1 for ele in l2)
    print(res)

if __name__ == '__main__':
    main()