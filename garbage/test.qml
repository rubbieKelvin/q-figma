import QtQuick 2.0
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.9
import QtQuick.Shapes 1.11

Rectangle{
	id: root
	width: 400.0
	height: 600.0
	visible: true
	color: Qt.rgba(0.20000000298023224, 0.20000000298023224, 0.20000000298023224, 1.0)

	Rectangle{
		id: frame_31333A31
		x: 0.0
		y: 0.0
		width: 400.0
		height: 45.0
		color: Qt.rgba(0.30980393290519714, 0.30980393290519714, 0.30980393290519714, 1.0)

		Label{
			id: text_31333A32
			x: 17.0
			y: 0.0
			width: 113.0
			height: 45.0
			text: qsTr("Test Application")
			font.family: "Montserrat"
			font.pixelSize: 12
			font.letterSpacing: 0.0
			lineHeight: 14.0625
			verticalAlignment: Text.AlignVCenter
			horizontalAlignment: Text.AlignLeft
			color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

		}

	}

	Rectangle{
		id: frame_31333A34
		x: 0.0
		y: 45.0
		width: 400.0
		height: 181.0
		color: Qt.rgba(0.5098039507865906, 0.5098039507865906, 0.5098039507865906, 1.0)

	}

	Rectangle{
		id: frame_31333A3134
		x: 25.0
		y: 203.0
		width: 351.0
		height: 110.0
		anchors.verticalCenter: parent.verticalCenter
		anchors.verticalCenterOffset: -42.0
		color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

		Rectangle{
			id: frame_31333A3131
			x: 0.0
			y: 0.0
			width: 109.0
			height: 110.0
			radius: 6.0
			color: Qt.rgba(0.30980393290519714, 0.30980393290519714, 0.30980393290519714, 1.0)

		}

		Rectangle{
			id: frame_31333A3132
			x: 121.0
			y: 0.0
			width: 109.0
			height: 110.0
			radius: 6.0
			color: Qt.rgba(0.30980393290519714, 0.30980393290519714, 0.30980393290519714, 1.0)

		}

		Rectangle{
			id: frame_31333A3133
			x: 242.0
			y: 0.0
			width: 109.0
			height: 110.0
			radius: 6.0
			color: Qt.rgba(0.30980393290519714, 0.30980393290519714, 0.30980393290519714, 1.0)

		}

	}

	Rectangle{
		id: frame_31333A3338
		x: 26.0
		y: 338.0
		width: 344.0
		height: 196.0
		anchors.horizontalCenter: parent.horizontalCenter
		anchors.horizontalCenterOffset: -2.0
		color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

		Rectangle{
			id: frame_31333A3233
			x: 0.0
			y: 0.0
			width: 344.0
			height: 50.0
			color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

			Rectangle{
				id: frame_31333A3135
				x: 0.0
				y: 0.0
				width: 50.0
				height: 50.0
				radius: 25.0
				color: Qt.rgba(0.30980393290519714, 0.30980393290519714, 0.30980393290519714, 1.0)

			}

			Label{
				id: text_31333A3136
				x: 58.0
				y: 9.0
				width: 207.0
				height: 15.0
				anchors.horizontalCenter: parent.horizontalCenter
				anchors.horizontalCenterOffset: -10.5
				text: qsTr("Item Name")
				font.family: "Montserrat"
				font.pixelSize: 12
				font.letterSpacing: 0.0
				lineHeight: 14.0625
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignLeft
				color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

			}

			Label{
				id: text_31333A3137
				x: 58.0
				y: 29.0
				width: 207.0
				height: 12.0
				anchors.horizontalCenter: parent.horizontalCenter
				anchors.horizontalCenterOffset: -10.5
				text: qsTr("this is a simple test for Qfigma")
				font.family: "Montserrat"
				font.pixelSize: 10
				font.letterSpacing: 0.0
				lineHeight: 11.71875
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignLeft
				color: Qt.rgba(0.7411764860153198, 0.7411764860153198, 0.7411764860153198, 1.0)

			}

			Rectangle{
				id: frame_31333A3230
				x: 279.0
				y: 9.0
				width: 65.0
				height: 30.0
				radius: 5.0
				gradient: LinearGradient {
					x1: 32.5
					y1: -9.184851394388759e-16
					x2: 32.5
					y2: 29.999999999999996
					GradientStop {position: 0.513788640499115; color: Qt.rgba(0.4541666805744171, 0.4541666805744171, 0.4541666805744171, 1.0)}
					GradientStop {position: 0.5138886570930481; color: Qt.rgba(0.36666667461395264, 0.36666667461395264, 0.36666667461395264, 1.0)}
				}

				Label{
					id: text_31333A3231
					x: 0.0
					y: 0.0
					width: 65.0
					height: 30.0
					text: qsTr("report")
					font.family: "Montserrat"
					font.pixelSize: 10
					font.letterSpacing: 0.0
					lineHeight: 11.71875
					verticalAlignment: Text.AlignVCenter
					horizontalAlignment: Text.AlignHCenter
					color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

				}

			}

		}

		Rectangle{
			id: frame_31333A3234
			x: 0.0
			y: 73.0
			width: 344.0
			height: 50.0
			color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

			Rectangle{
				id: frame_31333A3235
				x: 0.0
				y: 0.0
				width: 50.0
				height: 50.0
				radius: 25.0
				color: Qt.rgba(0.30980393290519714, 0.30980393290519714, 0.30980393290519714, 1.0)

			}

			Label{
				id: text_31333A3236
				x: 58.0
				y: 9.0
				width: 207.0
				height: 15.0
				anchors.horizontalCenter: parent.horizontalCenter
				anchors.horizontalCenterOffset: -10.5
				text: qsTr("Item Name")
				font.family: "Montserrat"
				font.pixelSize: 12
				font.letterSpacing: 0.0
				lineHeight: 14.0625
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignLeft
				color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

			}

			Label{
				id: text_31333A3237
				x: 58.0
				y: 29.0
				width: 207.0
				height: 12.0
				anchors.horizontalCenter: parent.horizontalCenter
				anchors.horizontalCenterOffset: -10.5
				text: qsTr("this is a simple test for Qfigma")
				font.family: "Montserrat"
				font.pixelSize: 10
				font.letterSpacing: 0.0
				lineHeight: 11.71875
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignLeft
				color: Qt.rgba(0.7411764860153198, 0.7411764860153198, 0.7411764860153198, 1.0)

			}

			Rectangle{
				id: frame_31333A3238
				x: 279.0
				y: 9.0
				width: 65.0
				height: 30.0
				radius: 5.0
				gradient: LinearGradient {
					x1: 32.5
					y1: -9.184851394388759e-16
					x2: 32.5
					y2: 29.999999999999996
					GradientStop {position: 0.513788640499115; color: Qt.rgba(0.4541666805744171, 0.4541666805744171, 0.4541666805744171, 1.0)}
					GradientStop {position: 0.5138886570930481; color: Qt.rgba(0.36666667461395264, 0.36666667461395264, 0.36666667461395264, 1.0)}
				}

				Label{
					id: text_31333A3239
					x: 0.0
					y: 0.0
					width: 65.0
					height: 30.0
					text: qsTr("report")
					font.family: "Montserrat"
					font.pixelSize: 10
					font.letterSpacing: 0.0
					lineHeight: 11.71875
					verticalAlignment: Text.AlignVCenter
					horizontalAlignment: Text.AlignHCenter
					color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

				}

			}

		}

		Rectangle{
			id: frame_31333A3330
			x: 0.0
			y: 146.0
			width: 344.0
			height: 50.0
			color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

			Rectangle{
				id: frame_31333A3331
				x: 0.0
				y: 0.0
				width: 50.0
				height: 50.0
				radius: 25.0
				color: Qt.rgba(0.30980393290519714, 0.30980393290519714, 0.30980393290519714, 1.0)

			}

			Label{
				id: text_31333A3332
				x: 58.0
				y: 9.0
				width: 207.0
				height: 15.0
				anchors.horizontalCenter: parent.horizontalCenter
				anchors.horizontalCenterOffset: -10.5
				text: qsTr("Item Name")
				font.family: "Montserrat"
				font.pixelSize: 12
				font.letterSpacing: 0.0
				lineHeight: 14.0625
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignLeft
				color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

			}

			Label{
				id: text_31333A3333
				x: 58.0
				y: 29.0
				width: 207.0
				height: 12.0
				anchors.horizontalCenter: parent.horizontalCenter
				anchors.horizontalCenterOffset: -10.5
				text: qsTr("this is a simple test for Qfigma")
				font.family: "Montserrat"
				font.pixelSize: 10
				font.letterSpacing: 0.0
				lineHeight: 11.71875
				verticalAlignment: Text.AlignVCenter
				horizontalAlignment: Text.AlignLeft
				color: Qt.rgba(0.7411764860153198, 0.7411764860153198, 0.7411764860153198, 1.0)

			}

			Rectangle{
				id: frame_31333A3334
				x: 279.0
				y: 9.0
				width: 65.0
				height: 30.0
				radius: 5.0
				gradient: LinearGradient {
					x1: 32.5
					y1: -9.184851394388759e-16
					x2: 32.5
					y2: 29.999999999999996
					GradientStop {position: 0.513788640499115; color: Qt.rgba(0.4541666805744171, 0.4541666805744171, 0.4541666805744171, 1.0)}
					GradientStop {position: 0.5138886570930481; color: Qt.rgba(0.36666667461395264, 0.36666667461395264, 0.36666667461395264, 1.0)}
				}

				Label{
					id: text_31333A3335
					x: 0.0
					y: 0.0
					width: 65.0
					height: 30.0
					text: qsTr("report")
					font.family: "Montserrat"
					font.pixelSize: 10
					font.letterSpacing: 0.0
					lineHeight: 11.71875
					verticalAlignment: Text.AlignVCenter
					horizontalAlignment: Text.AlignHCenter
					color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

				}

			}

		}

	}

	Label{
		id: text_31333A3337
		x: 174.0
		y: 581.0
		width: 52.0
		height: 12.0
		anchors.verticalCenter: parent.verticalCenter
		anchors.verticalCenterOffset: 287.0
		text: qsTr("rubbiesoft")
		font.family: "Montserrat"
		font.pixelSize: 10
		font.letterSpacing: 0.0
		lineHeight: 11.71875
		verticalAlignment: Text.AlignVCenter
		horizontalAlignment: Text.AlignLeft
		color: Qt.rgba(1.0, 1.0, 1.0, 1.0)

	}

}
