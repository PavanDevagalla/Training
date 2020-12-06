//Program to extends Framework

class SQLite extends Framework
{
	public SQLite() throws Exception
	{
		super("org.sqlite.JDBC", "jdbc:sqlite:D:/Training/JAVA/framework.db");
	}
}