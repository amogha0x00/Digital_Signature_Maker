import cv2
import numpy as np
import argparse
from os.path import exists


parser = argparse.ArgumentParser(description='Make Digital Signature')
parser.add_argument('PATH',
                    metavar='path_to_image',
                    type=str,
                    help='the path to the signature image')
parser.add_argument('-a',
                    '--auto',
                    action='store_true',
                    help='make signature with default settings and save it')
args = parser.parse_args()

PATH_TO_SIGNATURE = args.PATH

if not exists(PATH_TO_SIGNATURE):
    print('The path specified does not exist')
    quit()


def make_sig(signature_org, lower_threshold, blur_amount, auto=0):
    if auto: # cv2.THRESH_BINARY = 0
        auto = cv2.THRESH_OTSU # cv2.THRESH_OTSU = 8
        lower_threshold = 0
    ret, binary_sig = cv2.threshold(signature_org, lower_threshold, 255, auto)
    
    if blur_amount > 0:
        blur_amount = 2*blur_amount + 1 # (2*n + 1)
        blur_binary_sig = cv2.medianBlur(binary_sig, blur_amount)
    else:
        blur_binary_sig = binary_sig

    trans_sig = cv2.cvtColor(blur_binary_sig, cv2.COLOR_GRAY2BGRA)
    for row in trans_sig:
        for pixel in row:
            if pixel[0]:
                pixel[3] = 0
            else:
                pixel[3] = 255

    return blur_binary_sig, trans_sig

def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping, signature_org
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        # draw a rectangle around the region of interest
        cv2.rectangle(signature_org, refPt[0], refPt[1], 0, 2)
        cv2.imshow('Original Image', signature_org)


def make_show_sig(sig_file_name, lower_threshold=127, blur_amount=2, height=300, width=800):
    sig_name = sig_file_name.split('.')[0]
    global signature_org
    signature_org = cv2.imread(sig_file_name, 2)
    if args.auto:
        binary_sig , trans_sig = make_sig(signature_org, lower_threshold, blur_amount, auto=1)
        cv2.imwrite(sig_name + '_binary.png', binary_sig)
        cv2.imwrite(sig_name + '_trans.png', trans_sig)
        return 0
    should_crop = input("\nWhat to crop the image before making signature ? [y/ any]:- ").lower()
    if should_crop == 'y':
        global refPt, cropping
        refPt = []
        cropping = False
        clone_signature = signature_org.copy()
        cv2.namedWindow('Original Image')
        cv2.imshow('Original Image', signature_org)
        cv2.setMouseCallback('Original Image', click_and_crop)
        print('Usage: press r to reset the crop area\n\t   '
            'press c to crop (if you dont want to crop you can press c without selecting crop area or press x button)\n'
            'Due to Open cv limitaions larger images are not displayed correctly. In that case you may need to crop image on other software')
        while cv2.getWindowProperty('Original Image', cv2.WND_PROP_VISIBLE):
            cv2.imshow('Original Image', signature_org)
            key = cv2.waitKey(1) & 0xFF
            # if the 'r' key is pressed, reset the cropping region
            if key == ord("r"):
                signature_org = clone_signature.copy()
            # if the 'c' key is pressed, break from the loop
            elif key == ord("c"):
                break
        if len(refPt) == 2:
            refPt = np.array(refPt)
            [y,y1], [x,x1] = [refPt[:, 1], refPt[:, 0]]
            signature_org = clone_signature[y:y1, x:x1]
        else:
            signature_org = clone_signature
        cv2.destroyAllWindows()

    prev_l_t, prev_b_a = (0, 0)

    cv2.namedWindow('Your Digital Signature', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Your Digital Signature', width, height)
    cv2.createTrackbar('lower_threshold','Your Digital Signature',0,255, lambda x: None)
    cv2.createTrackbar('blur_amount','Your Digital Signature',0,25, lambda x: None)
    cv2.setTrackbarPos('lower_threshold','Your Digital Signature', lower_threshold)
    cv2.setTrackbarPos('blur_amount','Your Digital Signature', blur_amount)
    while cv2.getWindowProperty('Your Digital Signature', cv2.WND_PROP_VISIBLE):
        l_t =  cv2.getTrackbarPos('lower_threshold','Your Digital Signature')
        b_a = cv2.getTrackbarPos('blur_amount','Your Digital Signature')
        if (l_t != prev_l_t) or (b_a != prev_b_a):
            binary_sig , trans_sig = make_sig(signature_org, l_t, b_a)
            prev_l_t = l_t
            prev_b_a = b_a
        cv2.imshow("Your Digital Signature", trans_sig)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            cv2.setTrackbarPos('lower_threshold','Your Digital Signature', lower_threshold)
            cv2.setTrackbarPos('blur_amount','Your Digital Signature', blur_amount)
        if key == ord('s'):
            cv2.imwrite(sig_name + '_binary.png', binary_sig)
            cv2.imwrite(sig_name + '_trans.png', trans_sig) 
            break
        elif key == ord('q'):
            break
    cv2.destroyAllWindows()


make_show_sig(PATH_TO_SIGNATURE)
