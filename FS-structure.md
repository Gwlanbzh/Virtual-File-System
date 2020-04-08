# File System's structure

## Definitions.

The "blocks" we will be talking about are 512 octets large.

## 1. The sectors.

The file system will be made of :

  1. an allocation table.
  
  2. the root directory, and the other directories and files.

## 2. The allocation table.

In order to allow for a variable size of disk, the allocation table must be of a variable size, proportionnal to the disk's size. In order to know how large is this table, the first byte of the first block of the allocation table is used to store this size. Since it is 1 byte, its greatest value can be 65535, so the allocation table can be 65535 blocks large at the most. So, since 1 block can store the allocation information for 4096 block, the FS can be 4096 × 65535 = 268431360 blocks large at the most. We can deduce that the maximal size of a disk is 65535 + 268431360 = **268496895** blocks large, so **137470410240** bytes large. It is quite fair.

For each block, we must know if it is allocated or not; there is a table that records this information. The table's n-th bit records the information for the n-th block the second section (root directory and others). If the block is free, the the bit is set to `1`; else, it is set to `0`.

## 3. The files.

A file has mo metadata. It will be made of nothing else than the data it contains, and will be defined in the directories it is in (see .

### Directories.

A directory is a file, containing links to other files. Hence, a directory has got such a content:

```file1:emplacement+emplacement:[is_directory];file2:emplacement+emplacement:[is_directory]```

The files's definitions are surrounded by semicolons, and are made of its name, then the block in which it is (separated with `+`), then a \[is_directory] data: if it is set to `1`, the file defined is a directory; else, it is not. These three elements are separated with a semicolon.

#### The root directory.

Since it is the *root*, this directory cannot be defined in another directory. We take the convention that it is always made of the five first blocks of the file system.
