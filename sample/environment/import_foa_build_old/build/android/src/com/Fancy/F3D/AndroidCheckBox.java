package com.Fancy.F3D;

import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;

import com.Fancy.Application.UIGlobal;

public class AndroidCheckBox extends AndroidUI
{
	public BitmapDrawable mNormal;
	public BitmapDrawable mSelect;

	public void setImage( Bitmap normal, Bitmap select )
	{
		mNormal = new BitmapDrawable( normal );
		mSelect = new BitmapDrawable( select );
		UIGlobal.sendMessage( this, UIGlobal.CHECKBOX_IMAGE );
	}
	
	public void removeView( )
	{
		UIGlobal.sendMessage( this, UIGlobal.CHECKBOX_REMOVE );
	}
}