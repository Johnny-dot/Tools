package com.Fancy.Application;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;

public class Launcher extends Activity {
	@Override
	protected void onCreate( Bundle savedInstanceState ) 
	{
		super.onCreate( savedInstanceState );

		if ( UIGlobal.active == null )
		{
			Intent intent = new Intent(this, MainActivity.class);
			startActivity(intent);
		}

		finish();
	}
}
