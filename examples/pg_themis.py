#!/usr/bin/python3.5
#
# Copyright (c) 2016 Cossack Labs Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import postgresql
from pythemis import scell

#connect to bd
db = postgresql.open('pq://localhost:5432/test')

#load module
db.execute("CREATE EXTENSION IF NOT EXISTS pg_themis")

#scell encrypt by pg_themis
stmt = db.prepare("select pg_themis_scell_encrypt_seal($1::bytea, $2::bytea)")
enc_data = stmt.first(b"data", b"password")
print(enc_data)

#scell decrypt by pythemis
enc = scell.scell_seal(b"password")
data = enc.decrypt(enc_data)
print(data)

#scell encrypt by pythemis
enc_data = enc.encrypt(b"data2")
print(enc_data)

#scell decrypt by pg_themis
stmt = db.prepare("select pg_themis_scell_decrypt_seal($1::bytea, $2::bytea)")
print(stmt.first(enc_data, b"password"))


#smessage encrypt 
stmt = db.prepare("select pg_themis_smessage_encrypt($1::bytea, $2::bytea)")
enc_data = stmt.first(b"data", b"\x55\x45\x43\x32\x00\x00\x00\x2d\x6b\xbb\x79\x79\x03\xfa\xb7\x33\x3a\x4d\x6e\xb7\xc2\x59\xde\x78\x96\xfa\x69\xe6\x63\x86\x91\xc2\x65\xa0\x92\xf6\x5a\x22\x3c\xa9\x8e\xc9\xa7\x35\x42")
print(enc_data)

#smessage decrypt
stmt = db.prepare("select pg_themis_smessage_decrypt($1::bytea, $2::bytea)")
data = stmt.first(enc_data, b"\x52\x45\x43\x32\x00\x00\x00\x2d\xc7\xa8\xca\x7a\x00\xc3\xb5\xd1\xad\x51\x37\x30\x8f\x45\xe6\x5e\x54\xdf\x2b\x7a\x45\xbc\x85\x08\xe8\xcc\x3b\xc9\x48\x1b\x63\x1a\xe8\x12\x8b\x39\x74")
print(data)

#unload module
db.execute("DROP EXTENSION pg_themis")
