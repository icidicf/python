#!/usr/bin/python

import sys

srv_cfr_dict = {
'1':'CFR_REF_TYPE',
'2':'CFR_ID_TYPE',
'3':'CFR_SRV_FLOW_REF_TYPE',
'4':'CFR_SRV_FLOW_ID_TYPE',
'5':'CFR_RULE_PRIORITY_TYPE',
'6':'CFR_ACTIVATION_STATE_TYPE',
'7':'CFR_DSC_ACTION_TYPE',
'8':'CFR_ERRORENC_TYPE',
'9':'IP_PKT_CFR_TYPE',
'10':'DEST_PORT_END_TYPE'}

srv_flow_dict = {'1':'SRV_FLOW_REF_TYPE', '2':'SRV_FLOW_ID_TYPE',
 '3':'SRV_ID_TYPE',
 '4':'SRV_CLASS_NAME_TYPE',
 '5':'SRV_FLOW_ERRENC_TYPE',
 '6':'QOS_PARAM_SET_TYPE',
 '7':'TRF_PRIORITY_TYPE',
 '8':'MAX_SUSTAINED_RATE_TYPE',
 '9':'MAX_TRAF_BURST_TYPE',
 '10':'MIN_RSVD_TRAF_RATE_TYPE',
 '11':'MIN_RSVD_RATE_PKT_SZ_TYPE',
 '12':'ACTIVE_QOS_PARAM_TIMEOUT_TYPE',
 '13':'ADMIT_QOS_PARAM_TIMEOUT_TYPE',
 '14':'MAX_CONCAT_BURST_TYPE',
 '15':'SRV_FLOW_SCHED_TYPE',
 '16':'REQ_TRANS_POLICY_TYPE',
 '17':'NOMINAL_POLL_INTVL_TYPE',
 '18':'TOLERATED_POLL_JITTER_TYPE',
 '19':'UNSOLC_GRANT_SIZE_TYPE',
 '20':'NOMINAL_GRANT_INTVL_TYPE',
 '21':'TOLERATED_GRANT_JITTER_TYPE',
 '22':'GRANTS_PER_INTVL_TYPE',
 '23':'IP_TOS_OVERWRITE_TYPE',
 '24':'UNSOLC_GTIME_REF_TYPE',
 '25':'MULTIPLIER_CR_WINDOW_TYPE',
 '26':'MULTIPLIER_BYTE_REQ_TYPE',
 '31':'REQUIRED_MASK_TYPE',
 '32':'FORBIDDEN_MASK_TYPE',
 '33':'AGGREGATE_MASK_TYPE',
 '34':'APPLICATION_ID_TYPE'}


nest_depth=1

def chunk_with_specified_width(string, length):
	return (string[i+0: i+length] for i in range(0, len(string), length))


def process_tlv(tlv, indent):
	cur_pos = 0
	total_len = len(tlv)
	while cur_pos  < total_len:
		output = ""
		cur_type = int(tlv[cur_pos], 16)
		cur_len = int(tlv[cur_pos+1], 16)
		print "type is %d, len is %d"  % (cur_type, cur_len)
		sub_tlv = tlv[cur_pos + 2 : cur_pos + 2 + cur_len]
#		print "indent %u cur pos %d , cur len %d curr pos %u  " % ( indent, cur_pos ,cur_len, cur_pos + 2 + cur_len)
		for it in sub_tlv:
			output = output + it
		print "\t"*indent + output
		cur_pos = cur_pos + 2 + cur_len
		if indent < nest_depth:
			process_tlv(sub_tlv, (indent + 1))
    

if __name__=="__main__":
	if not len(sys.argv) > 1:
		print "please give tlv string "

	input_tlv = sys.argv[1]
	#item =list(chunk_with_specified_width(input_tlv, 2)) 
	#for it in item:
	#	print "index   content ",  it, "more" 
	
	process_tlv(item, 0)
