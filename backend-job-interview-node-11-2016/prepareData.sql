create table customers(
  cid int,
  name varchar(100),
  primary key (cid)
);

create table invoices(
  id int,
  name varchar(100),
  cid int,
  primary key (id),
  foreign key (cid) references customers(cid)
);

insert into customers (name, cid) values ('user1',1);
insert into customers (name, cid) values ('user2',2);
insert into customers (name, cid) values ('user3',3);

insert into invoices (id, name, cid) values(1, 'bill1', 1);
insert into invoices (id, name, cid) values(2, 'bill2', 1);
insert into invoices (id, name, cid) values(3, 'bill3', 3);
insert into invoices (id, name, cid) values(4, 'bill5', 3);
