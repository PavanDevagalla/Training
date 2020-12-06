//Program to extends Framework

class MySQL extends Framework
{

	public MySQL() throws Exception
	{
		super("com.mysql.cj.jdbc.Driver", "jdbc:mysql://165.22.14.77/dbPavan?user=Pavankumar&password=Pavankumar");
	}

}