package com.Fancy.F3D;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;

import com.Fancy.Application.UIGlobal;

public class AndroidPanel extends AndroidUI
{
	public BitmapDrawable mImage;

	public void setImage( Bitmap normal )
	{
		mImage = new BitmapDrawable( normal );
		UIGlobal.sendMessage( this, UIGlobal.PANEL_IMAGE );
	}

	public void removeView( )
	{
		UIGlobal.sendMessage( this, UIGlobal.PANEL_REMOVE );
	}
}