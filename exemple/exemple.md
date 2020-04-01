# exemple disk file :

The first block is a table where each byte represent a block. If the byte is 00, the corresponding block is free and if the byte is 01, the corresponding block is taken.

The second block is the root directory.

If the first bytes of each blocks is 00, the block is a dir, if the byte is 01, the block is a file.

the following exemple can be represent like that :

```
 /
 ├── dir1
 │   └── sub_dir1
 │       
 └── dir2
     └── file1
```

## bloc 0 :

![Bloc1](bloc1.png)

## bloc 1 :

![Bloc2](bloc2.png)

## bloc 2 :

![Bloc3](bloc3.png)

## bloc 3 :

![Bloc4](bloc4.png)

## bloc 4 :

![Bloc5](bloc5.png)

## bloc 5 :

![Bloc5](bloc6.png)
