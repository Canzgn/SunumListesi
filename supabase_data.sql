docker : pg_dump: error: aborting because of server version mismatch
At line:1 char:1
+ docker compose exec db pg_dump "postgresql://postgres.ifadadkcrfwmmhz ...
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (pg_dump: error:...ersion mismatch 
   :String) [], RemoteException
    + FullyQualifiedErrorId : NativeCommandError
 
pg_dump: detail: server version: 17.6; pg_dump version: 16.13
